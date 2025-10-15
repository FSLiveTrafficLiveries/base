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

    // NOTE:  This is the original code that lists all aircraft individually
    //
    // const dir = fs.opendirSync(simObjectsBaseDir);
    // let dirent;
    // while ((dirent = dir.readSync()) !== null) {
    //   aircraftobjects.push({
    //     name: `${dirent.name.replace("FSLTL_", "")}`,
    //     sourceDir: `${simObjectsDir}${dirent.name}`,
    //   });
    // }
    // dir.closeSync();

    // NEW: Group aircraft by the model type in the directory name
    const dir = fs.opendirSync(simObjectsBaseDir);
    let dirent;
    const groupedAircraft = {};

    while ((dirent = dir.readSync()) !== null) {
      const dirName = dirent.name;
      // Ensure the directory name is long enough
      if (dirName.length >= 10) {
        const underscoreIndices = [];
        for (let i = 0; i < dirName.length; i++) {
          if (dirName[i] === "_") underscoreIndices.push(i);
        }
        let groupKey;
        if (underscoreIndices.length >= 2) {
          groupKey = dirName.substring(underscoreIndices[0] + 1, underscoreIndices[1]);
        } else if (underscoreIndices.length === 1) {
          groupKey = dirName.substring(underscoreIndices[0] + 1);
        } else {
          groupKey = dirName; // fallback if no underscores
        }
        groupKey = groupKey.toUpperCase();
        if (!groupedAircraft[groupKey]) {
          groupedAircraft[groupKey] = [];
          console.log(`Creating group for ICAO: ${groupKey}`); // Log when a new group is created
        }
        groupedAircraft[groupKey].push({
          name: dirName.replace("FSLTL_", ""),
          sourceDir: `${simObjectsDir}${dirName}`,
        });
      }
      else {
        console.warn(`Directory name "${dirName}" is too short to extract ICAO code.`);
      }
    }
    dir.closeSync();

    // Add each grouped aircraft to aircraftobjects by each groupKey
    Object.keys(groupedAircraft).forEach(groupKey => {
      aircraftobjects.push({
      name: groupKey,
      sourceDir: groupedAircraft[groupKey].map(obj => obj.sourceDir),
      });
    });

    // This was added to create the draft 1.6 release... where all Lioveries are one large module
    //
    // Liveries all in one assset
    // aircraftobjects.push({
    //   name: "Liveries",
    //   sourceDir: simObjectsDir,
    // });

    aircraftobjects.push({
      name: "FLIGHTAWARE-FIX",
      sourceDir: "./AirTraffic",
    });
    aircraftobjects.push({ name: "MISC", sourceDir: "./ModelBehaviorDefs" });

    // Log to cnsole the aircraft objects for verification the sourceDirs are correct
    aircraftobjects.forEach((obj, idx) => {
      console.log(`Aircraft Object ${idx + 1}:`, obj);
    });

    // Comment out the actual packing for now
    //
    // const result = await fragmenter.pack({
    //   version: version,
    //   baseDir: baseDir,
    //   outDir: outputDir,
    //   modules: aircraftobjects,
    //   packOptions: {
    //     useConsoleLog: true,
    //     forceCacheBust: false,
    //     splitFileSize: 536_870_912,
    //     keepCompleteModulesAfterSplit: false,
    //     noBaseCopy: true,
    //   },
    // });
    // console.log(result);
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
};

execute();
