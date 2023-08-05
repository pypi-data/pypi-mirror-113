Object.defineProperty(exports, "__esModule", { value: true });
exports.createFuzzySearch = exports.loadFuzzySearch = void 0;
var tslib_1 = require("tslib");
var constants_1 = require("app/constants");
function loadFuzzySearch() {
    return Promise.resolve().then(function () { return tslib_1.__importStar(require('fuse.js')); });
}
exports.loadFuzzySearch = loadFuzzySearch;
function createFuzzySearch(objects, options) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var Fuse, opts;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!options.keys) {
                        throw new Error('You need to define `options.keys`');
                    }
                    return [4 /*yield*/, loadFuzzySearch()];
                case 1:
                    Fuse = (_a.sent()).default;
                    opts = tslib_1.__assign(tslib_1.__assign({}, constants_1.DEFAULT_FUSE_OPTIONS), options);
                    return [2 /*return*/, new Fuse(objects, opts)];
            }
        });
    });
}
exports.createFuzzySearch = createFuzzySearch;
//# sourceMappingURL=createFuzzySearch.jsx.map