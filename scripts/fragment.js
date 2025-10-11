const fragmenter = require("@flybywiresim/fragmenter");
const fs = require("fs");

const execute = async () => {
  try {
    const baseDir = "fsltl-traffic-base";
    const outputDir = "fsltl-traffic-base-build";
    const simObjectsBaseDir = baseDir + "/SimObjects/Airplanes";
    const simObjectsDir = "./SimObjects/Airplanes/";
    const version = process.env.GITHUB_REF_NAME;

    let aircraftobjects = [];

    // const dir = fs.opendirSync(simObjectsBaseDir);
    // let dirent;
    // while ((dirent = dir.readSync()) !== null) {
    //   aircraftobjects.push({
    //     name: `${dirent.name.replace("FSLTL_", "")}`,
    //     sourceDir: `${simObjectsDir}${dirent.name}`,
    //   });
    // }
    // dir.closeSync();

    // Testing adding all liveries together, hoping the splitfileSize will handle it
    // aircraftobjects.push({
    //   name: "Liveries",
    //   sourceDir: simObjectsBaseDir,
    // });

    // Pair up directories that start with the same first 10 characters
    
    const dir = fs.opendirSync(simObjectsBaseDir);
    let dirent;
    const dirGroups = {};

    while ((dirent = dir.readSync()) !== null) {
      if (dirent.isDirectory()) {
        const prefix = dirent.name.substring(0, 10);
        if (!dirGroups[prefix]) {
          dirGroups[prefix] = [];
        }
        dirGroups[prefix].push(dirent.name);
      }
    }
    dir.closeSync();

    // Push all groups to aircraftobjects, even if length is 1
    Object.values(dirGroups).forEach(group => {
      aircraftobjects.push({
        name: `${prefix}_GROUP`,
        sourceDir: group.map(name => `${simObjectsDir}${name}`),
      });
    });

    aircraftobjects.push({
      name: "FLIGHTAWARE-FIX",
      sourceDir: "./AirTraffic",
    });
    aircraftobjects.push({ name: "MISC", sourceDir: "./ModelBehaviorDefs" });

    const result = await fragmenter.pack({
      version: version,
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


