# Engine and buyer data are physically separate; updates replace only the engine

The product ships as a copyable Claude Code plugin and updates by drop-in replacement (zip) or marketplace reinstall. The buyer's Brand Profile and the Style Packs they author are their irreplaceable work.

Decision: the Engine folder (templates, starter packs, scripts, the authoring logic) and the buyer's data (Brand Profile + custom Style Packs, which live in the buyer's own project) are kept in physically separate locations. An update overwrites only the Engine folder and never touches buyer data. This is what makes the update story safe across both distribution channels (public marketplace and zip-from-storefront).

The explicit no: starter packs and the Brand Profile template ship inside the Engine, but a buyer's INSTANCE of their Brand Profile and their authored packs must never be written inside the Engine folder, or the next update wipes them.
