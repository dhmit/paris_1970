// SVGs that we're using as plain URLs
declare module '*.svg?url' {
  const content: string;
  export default content;
}

// SVGs that we're turning into SVG Elements and inlining
declare module '*.svg' {
  import React = require('react');
  export const ReactComponent: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  const src: string;
  export default src;
}

declare module "*.jpeg" {
  const value: any;
  export = value;
}

declare module "*.jpg" {
  const value: any;
  export = value;
}

declare module "*.png" {
  const value: any;
  export = value;
}


