Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var merge_1 = tslib_1.__importDefault(require("lodash/merge"));
/**
 * Drawing grid in rectangular coordinates
 *
 * e.g. alignment of your chart?
 */
function Grid(props) {
    if (props === void 0) { props = {}; }
    return merge_1.default({
        top: 20,
        bottom: 20,
        // This should allow for sufficient space for Y-axis labels
        left: '0%',
        right: '0%',
        containLabel: true,
    }, props);
}
exports.default = Grid;
//# sourceMappingURL=grid.jsx.map