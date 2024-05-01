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

// Open the database with custom index
const db = await orbitdb.open(remoteDBAddress, {
    Database: Documents({ indexBy: 'hash' })
});


const doc = {
    hash: 'unique-key',
    name: 'rest2',
    content: 'sdfsdre',
    // Other key-value pairs...
};

await db.put(doc)

for await (const res of db.iterator()) {
    console.log(res)
}

process.on('SIGINT', async () => {
    console.log("exiting...")

    await db.close()
    await orbitdb.stop()
    await ipfs.stop()
    process.exit(0)
})
