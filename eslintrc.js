// This file is _only_ here to tell ts-server on Windows where the tsconfig file lives
module.exports =
{
    extends: [".eslint.json"],
    parserOptions: {
        tsconfigRootDir: __dirname,
    },
};
