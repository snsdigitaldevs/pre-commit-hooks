#!/usr/bin/env node

const fs = require('fs');
const { program } = require('commander');

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

program.argument('[string...]').parse();

const args = program.args;

const commitMsgFile = args.pop();
const supportedTypes = args.length === 0 ? COMMIT_TYPE : args;

const commitMessage = fs.readFileSync(commitMsgFile, 'utf-8').trim();

const ticketPattern = `(((${TICKET_PREFIX.join('|')})-\\d+)|N/A)`;
const typePattern = `(${supportedTypes.join('|')})`;

const regex = new RegExp(`^${ticketPattern} ${typePattern}: .+$`);

const result = regex.test(commitMessage);

if (!result) {
  console.log(
    `
        Invalid commit message. please follow this template:   
            ticket type: message(TO-123 feat: message).
        Ticket: ${TICKET_PREFIX.join(', ')}
        Type: ${supportedTypes.join(', ')}
        `
  );
}

process.exit(regex.test(commitMessage) ? 0 : 1);