Object.defineProperty(exports, "__esModule", { value: true });
exports.loadFixtures = void 0;
var tslib_1 = require("tslib");
/* global __dirname */
/* eslint import/no-nodejs-modules:0 */
var fs_1 = tslib_1.__importDefault(require("fs"));
var path_1 = tslib_1.__importDefault(require("path"));
var FIXTURES_ROOT = path_1.default.join(__dirname, '../../fixtures');
/**
 * Loads a directory of fixtures. Supports js and json fixtures.
 */
function loadFixtures(dir, opts) {
    if (opts === void 0) { opts = {}; }
    var from = path_1.default.join(FIXTURES_ROOT, dir);
    var files = fs_1.default.readdirSync(from);
    var fixturesPairs = files.map(function (file) {
        var filePath = path_1.default.join(from, file);
        if (/[jt]sx?$/.test(file)) {
            var module_1 = require(filePath);
            if (Object.keys(module_1).includes('default')) {
                throw new Error('Javascript fixtures cannot use default export');
            }
            return [file, module_1];
        }
        if (/json$/.test(file)) {
            return [file, JSON.parse(fs_1.default.readFileSync(filePath).toString())];
        }
        throw new Error("Invalid fixture type found: " + file);
    });
    var fixtures = Object.fromEntries(fixturesPairs);
    if (opts.flatten) {
        return Object.values(fixtures).reduce(function (acc, val) { return (tslib_1.__assign(tslib_1.__assign({}, acc), val)); }, {});
    }
    return fixtures;
}
exports.loadFixtures = loadFixtures;
//# sourceMappingURL=loadFixtures.js.map