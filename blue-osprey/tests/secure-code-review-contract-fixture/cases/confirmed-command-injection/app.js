const { execFile } = require("node:child_process");

function runReport(req, res) {
  const reportName = req.query.name;
  execFile("sh", ["-c", `generate-report --name ${reportName}`], (error, stdout) => {
    if (error) return res.status(500).send("report failed");
    res.type("text/plain").send(stdout);
  });
}

module.exports = { runReport };
