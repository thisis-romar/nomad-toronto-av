// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// Static output. Cloudflare Pages serves the built `dist/` and runs the edge
// auth layer in `functions/` (Pages Functions) in front of every request.
export default defineConfig({
  output: "static",
  trailingSlash: "ignore",
  integrations: [
    starlight({
      title: "NOMAD Toronto",
      description:
        "Private operations portal for the NOMAD Toronto AV system — for venue management.",
      tagline: "Venue operations portal",
      customCss: ["./src/styles/portal.css"],
      pagination: false,
      sidebar: [
        { label: "Welcome", link: "/" },
        { label: "Audio System", autogenerate: { directory: "audio" } },
        { label: "Log out", link: "/api/logout", attrs: { rel: "nofollow" } },
      ],
    }),
  ],
});
