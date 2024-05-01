import { createHelia } from 'helia';
import { createOrbitDB, Documents, OrbitDBAccessController } from '@orbitdb/core';
import { createLibp2p } from 'libp2p';
import { LevelBlockstore } from 'blockstore-level';
import { Libp2pOptions } from './config/libp2p.js';
import fs from 'fs';
import readline from 'readline';

const id = 1;

const blockstore = new LevelBlockstore(`./ipfs/${id}`);

const libp2p = await createLibp2p(Libp2pOptions);

const ipfs = await createHelia({ libp2p, blockstore });

const orbitdb = await createOrbitDB({ ipfs, id: `nodejs-${id}`, directory: `./orbitdb/${id}` });

// Open the database with custom index
const db = await orbitdb.open('my-docs', {
    Database: Documents({ indexBy: 'hash' }),
    AccessController: OrbitDBAccessController({ write: ['*'] })
});

console.log(db.address);

async function loadJsonData(filePath) {
    console.time('DataLoadingTime'); // Start time measurement

    const initialMemoryUsage = process.memoryUsage(); // Initial memory usage
    const initialCpuUsage = process.cpuUsage(); // Initial CPU usage

    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    // let counter = 1;
    for await (const line of rl) {
        // if (counter > 10) {
        //     break;
        // }
        try {
            const json = JSON.parse(line);
            await db.put(json);
        } catch (e) {
            console.error(`Error parsing JSON from file: ${e.message}`);
        }
        //counter++;
    }

    const finalMemoryUsage = process.memoryUsage(); // Final memory usage
    const finalCpuUsage = process.cpuUsage(initialCpuUsage); // Final CPU usage

    console.timeEnd('DataLoadingTime'); // End time measurement

    // Calculate and log memory usage
    const memoryUsage = {
        rss: finalMemoryUsage.rss - initialMemoryUsage.rss,
        heapTotal: finalMemoryUsage.heapTotal - initialMemoryUsage.heapTotal,
        heapUsed: finalMemoryUsage.heapUsed - initialMemoryUsage.heapUsed,
        external: finalMemoryUsage.external - initialMemoryUsage.external,
    };
    console.log('Memory Usage:', memoryUsage);

    // Log CPU usage
    console.log('CPU Usage:', finalCpuUsage);
}

console.log("starting to load data");

// Replace 'eth_data.json' with the path to your JSON file
await loadJsonData('eth_data.json');

async function queryDb() {
    console.time('QueryExecutionTime'); // Start time measurement

    const initialMemoryUsage = process.memoryUsage(); // Initial memory usage
    const initialCpuUsage = process.cpuUsage(); // Initial CPU usage

    const results = await db.query((doc) => doc.gas > 90000);

    const finalMemoryUsage = process.memoryUsage(); // Final memory usage
    const finalCpuUsage = process.cpuUsage(initialCpuUsage); // Final CPU usage

    console.timeEnd('QueryExecutionTime'); // End time measurement

    // Calculate and log memory usage
    const memoryUsage = {
        rss: finalMemoryUsage.rss - initialMemoryUsage.rss,
        heapTotal: finalMemoryUsage.heapTotal - initialMemoryUsage.heapTotal,
        heapUsed: finalMemoryUsage.heapUsed - initialMemoryUsage.heapUsed,
        external: finalMemoryUsage.external - initialMemoryUsage.external,
    };
    console.log('Memory Usage:', memoryUsage);

    // Log CPU usage
    console.log('CPU Usage:', finalCpuUsage);

    // console.log(results);
}

console.log("querying data");
// Call the async function
queryDb();

process.on('SIGINT', async () => {
    console.log("exiting...");

    await db.close();
    await orbitdb.stop();
    await ipfs.stop();
    process.exit(0);
});
