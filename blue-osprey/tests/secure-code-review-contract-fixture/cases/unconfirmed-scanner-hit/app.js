function createHash(value) {
  // The value is an internal constant in this fixture; no request reaches it.
  return require("node:crypto").createHash("md5").update(value).digest("hex");
}

module.exports = { createHash };
