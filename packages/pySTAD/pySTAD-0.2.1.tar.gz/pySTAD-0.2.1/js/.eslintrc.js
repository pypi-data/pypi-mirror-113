module.exports = {
    root: true,
    extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/eslint-recommended',
        'plugin:@typescript-eslint/recommended',
    ],
    parser: '@typescript-eslint/parser',
    parserOptions: {
      project: 'tsconfig.json',
      ecmaVersion: 2020,
      sourceType: 'module'
    },
    env: {
      es6: true,
      browser: true,
      node : true
    },
    plugins: [
      '@typescript-eslint',
      'svelte3',
    ],
    overrides: [
      {
        files: ['*.svelte'],
        processor: 'svelte3/svelte3',
      }
    ],
    rules: {
      '@typescript-eslint/indent': ['error', 2 ],
      '@typescript-eslint/linebreak-style': ['error', 'unix'],
      '@typescript-eslint/no-unused-vars': ['warn', { args: 'none' }],
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-namespace': 'off',
      '@typescript-eslint/no-use-before-define': 'off',
      '@typescript-eslint/quotes': [
        'error',
        'single',
        { avoidEscape: true, allowTemplateLiterals: false }
      ],
      'indent': ['error', 2 ],
      'linebreak-style': ['error', 'unix'],
      'quotes': ['error', 'single'],
      'semi': ['error', 'always'],
      'no-console': 'off',
      'no-unused-vars': ['warn', { args: 'none' }]
    }
  };