/**
 * A simple nodejs script which launches an orbitdb instance and creates a db 
 * with a single record.
 * 
 * To run from the terminal:
 * 
 * ```bash
 * node index.js
 * ```
 * or
 * ```bash
 * node index.js /orbitdb/<hash>
 * ```
 */
import { createHelia } from 'helia'
import { createOrbitDB, Documents, OrbitDBAccessController } from '@orbitdb/core'
import { createLibp2p } from 'libp2p'
import { LevelBlockstore } from 'blockstore-level'
import { Libp2pOptions } from './config/libp2p.js'

const id = 2

const blockstore = new LevelBlockstore(`./ipfs/${id}`)

const libp2p = await createLibp2p(Libp2pOptions)

const ipfs = await createHelia({ libp2p, blockstore })

const remoteDBAddress = process.argv.pop()

const orbitdb = await createOrbitDB({ ipfs, id: `nodejs-${id}`, directory: `./orbitdb/${id}` });

// Open the database with custom index
const db = await orbitdb.open(remoteDBAddress, {
    Database: Documents({ indexBy: 'hash' })
});



async function updateDocument(hash, updateFunction) {
    // Retrieve the current document by its hash
    const doc = await db.get(hash);

    if (doc) {
        // Modify the document using the provided updateFunction
        const updatedDoc = updateFunction(doc);

        // Ensure the hash field is preserved in the updated document
        await db.put({ ...updatedDoc, hash });

        console.log("Updated Document:", await db.get(hash));
    } else {
        console.log(`Document with hash ${hash} not found.`);
    }
}

async function main() {
    let doc = await db.get("0x8b2d2ea8653414788f7d738796587b2aef10a40d1f31ca162adfe8610674b8fc");
    console.log("Original Document:", doc);

    await updateDocument('0x8b2d2ea8653414788f7d738796587b2aef10a40d1f31ca162adfe8610674b8fc', (doc) => {
        // Modify the document as required
        doc.gas = 10;
        return doc;
    });

    // for await (const res of db.iterator()) {
    //     console.log(res)
    // }
}

main().catch(console.error);

async function printFirstFewEntries(db, numberOfEntries) {
    let count = 0;
    for await (const entry of db.iterator()) {
        console.log(entry.value); // Assuming you want to print the value of each entry
        count++;
        if (count >= numberOfEntries) break; // Stop after printing the specified number of entries
    }
}

// console.log("printing");
// // Example usage:
// await printFirstFewEntries(db, 5); // Prints the first 5 entries
// console.log("done");

process.on('SIGINT', async () => {
    console.log("exiting...");

    await db.close();
    await orbitdb.stop();
    await ipfs.stop();
    process.exit(0);
});