const fragmenter = require("@flybywiresim/fragmenter");
const fs = require("fs");

const execute = async () => {
  try {
    const baseDir = "fsltl-traffic-base";
    const outputDir = "fsltl-traffic-base-build";
    const simObjectsBaseDir = baseDir + "/SimObjects/Airplanes";
    const simObjectsDir = "./SimObjects/Airplanes/";

    let aircraftobjects = [];

    const dir = fs.opendirSync(simObjectsBaseDir);
    let dirent;
    while ((dirent = dir.readSync()) !== null) {
      aircraftobjects.push({
        name: `${dirent.name.replace("FSLTL_", "")}`,
        sourceDir: `${simObjectsDir}${dirent.name}`,
      });
    }
    dir.closeSync();
    aircraftobjects.push({
      name: "FLIGHTAWARE-FIX",
      sourceDir: "./AirTraffic",
    });
    aircraftobjects.push({ name: "MISC", sourceDir: "./ModelBehaviorDefs" });

    const result = await fragmenter.pack({
      baseDir: baseDir,
      outDir: outputDir,
      modules: aircraftobjects,
      packOptions: {
        useConsoleLog: true,
        forceCacheBust: false,
        splitFileSize: 536_870_912,
        keepCompleteModulesAfterSplit: false,
        noBaseCopy: true,
      },
    });
    console.log(result);
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
};

execute();
