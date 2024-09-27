#!/usr/bin/env node

import * as fs from 'fs';

const TICKET_PREFIX = ['TO', 'ECS', 'P20E'];

const COMMIT_TYPE = [
    'build',
    'chore',
    'ci',
    'docs',
    'feat',
    'fix',
    'perf',
    'refactor',
    'revert',
    'style',
    'test',
];

const commitMsgFile = process.argv[2];

const commitMessage = fs.readFileSync(commitMsgFile, 'utf-8').trim();

const ticketPattern = `(((${TICKET_PREFIX.join('|')})-\\d+)|N/A)`;
const typePattern = `(${COMMIT_TYPE.join('|')})`;

const regex = new RegExp(`^${ticketPattern} ${typePattern}: .+$`);

const result = regex.test(commitMessage);

if (!result) {
    console.log(
        `
        Invalid commit message. please follow this template:   
            ticket type: message(TO-123 feat: message).
        Ticket: ${TICKET_PREFIX.join(', ')}
        Type: ${COMMIT_TYPE.join(', ')}
        `
    );
}

process.exit(regex.test(commitMessage) ? 0 : 1);