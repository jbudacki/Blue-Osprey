function lookupUser(req, res) {
  const userId = String(req.query.userId || "");
  if (!/^[0-9a-f]{32}$/i.test(userId)) {
    return res.status(400).send("invalid user id");
  }
  return res.json({ userId });
}

module.exports = { lookupUser };
