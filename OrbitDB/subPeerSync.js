import { createHelia } from 'helia'
import { createOrbitDB, Documents } from '@orbitdb/core'
import { createLibp2p } from 'libp2p'
import { LevelBlockstore } from 'blockstore-level'
import { Libp2pOptions } from './config/libp2p.js'

const id = 2

const blockstore = new LevelBlockstore(`./ipfs/${id}`)

const libp2p = await createLibp2p(Libp2pOptions)

const ipfs = await createHelia({ libp2p, blockstore })

const remoteDBAddress = process.argv.pop()

const orbitdb = await createOrbitDB({ ipfs, id: `nodejs-${id}`, directory: `./orbitdb/${id}` });

// Variables to measure sync time
let syncStartTime;
let syncEndTime;

const db = await orbitdb.open(remoteDBAddress, {
    Database: Documents({ indexBy: 'hash' })
});

// When the database is ready (loaded from disk or first replicated)
db.events.on('join', () => {
    console.log("Database is ready.");
    syncEndTime = Date.now();
    const syncDuration = syncEndTime - syncStartTime;
    console.log(`Time taken to sync: ${syncDuration} ms`);
});

// When the database has replicated new data
db.events.on('replicated', () => {
    console.log("Database has replicated new data.");
});

// Start measuring the sync time
syncStartTime = Date.now();

// Additional operations...

process.on('SIGINT', async () => {
    console.log("Exiting...");

    await db.close();
    await orbitdb.stop();
    await ipfs.stop();
    process.exit(0);
});
