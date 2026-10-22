function exportRecords(records, destination) {
  if (!Array.isArray(records)) throw new TypeError("records must be an array");
  return destination.write(JSON.stringify(records));
}

module.exports = { exportRecords };
