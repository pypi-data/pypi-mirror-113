Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var platforms_1 = tslib_1.__importDefault(require("app/data/platforms"));
function getPlatformName(platform) {
    var platformData = platforms_1.default.find(function (_a) {
        var id = _a.id;
        return platform === id;
    });
    return platformData ? platformData.name : null;
}
exports.default = getPlatformName;
//# sourceMappingURL=getPlatformName.jsx.map