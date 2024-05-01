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
import { createOrbitDB, OrbitDBAccessController } from '@orbitdb/core'
import { createLibp2p } from 'libp2p'
import { LevelBlockstore } from 'blockstore-level'
import { Libp2pOptions } from './config/libp2p.js'

const id = 1

const blockstore = new LevelBlockstore(`./ipfs/${id}`)

const libp2p = await createLibp2p(Libp2pOptions)

const ipfs = await createHelia({ libp2p, blockstore })

const orbitdb = await createOrbitDB({ ipfs, id: `nodejs-${id}`, directory: `./orbitdb/${id}` })

let db

db = await orbitdb.open('nodejs', { AccessController: OrbitDBAccessController({ write: ['*'] }) })

console.log(db.address)

db.events.on('update', event => {
    console.log('update', event)
})

await db.add(`hello world from peer ${id}`)

process.on('SIGINT', async () => {
    console.log("exiting...")

    await db.close()
    await orbitdb.stop()
    await ipfs.stop()
    process.exit(0)
})
