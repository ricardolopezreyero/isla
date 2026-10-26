// RLR · Verificar un pase del Login de CapitalTorreon (copia de login-capitaltorreon/publico/verificar.js).
// Única diferencia: verificarPase(pase, aud, jwksPrueba) acepta una llave pública de prueba que SÓLO existe en
// .dev.vars (JWKS_PRUEBA) para probar en local sin la llave real. En producción esa variable no existe.
const EMISOR = "https://login.capitaltorreon.com";
let jwksCache = null, jwksT = 0;
async function jwks() { if (!jwksCache || Date.now() - jwksT > 3600000) { jwksCache = await (await fetch(EMISOR + "/.well-known/jwks.json")).json(); jwksT = Date.now(); } return jwksCache; }
export async function verificarPase(pase, aud, jwksPrueba) {
  if (typeof pase !== "string") return null;
  const [h, p, s] = pase.split("."); if (!h || !p || !s) return null;
  const de = (x) => Uint8Array.from(atob(x.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0));
  let cab, cuerpo; try { cab = JSON.parse(new TextDecoder().decode(de(h))); cuerpo = JSON.parse(new TextDecoder().decode(de(p))); } catch { return null; }
  if (cab.alg !== "ES256" || cuerpo.iss !== EMISOR || !(cuerpo.exp > Date.now() / 1000)) return null;
  if (aud && !(Array.isArray(aud) ? aud.includes(cuerpo.aud) : cuerpo.aud === aud)) return null;
  let llaves; try { llaves = jwksPrueba ? JSON.parse(jwksPrueba) : await jwks(); } catch { return null; }
  const jwk = (llaves.keys || []).find((k) => k.kid === cab.kid); if (!jwk) return null;
  try {
    const key = await crypto.subtle.importKey("jwk", jwk, { name: "ECDSA", namedCurve: "P-256" }, false, ["verify"]);
    const ok = await crypto.subtle.verify({ name: "ECDSA", hash: "SHA-256" }, key, de(s), new TextEncoder().encode(h + "." + p));
    return ok ? cuerpo : null;
  } catch { return null; }
}
