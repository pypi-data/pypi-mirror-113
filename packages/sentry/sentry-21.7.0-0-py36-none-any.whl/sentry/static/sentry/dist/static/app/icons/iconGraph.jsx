Object.defineProperty(exports, "__esModule", { value: true });
exports.IconGraph = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var iconGraphBar_1 = require("./iconGraphBar");
var iconGraphCircle_1 = require("./iconGraphCircle");
var iconGraphLine_1 = require("./iconGraphLine");
var IconGraph = React.forwardRef(function IconGraph(_a, ref) {
    var _b = _a.type, type = _b === void 0 ? 'line' : _b, props = tslib_1.__rest(_a, ["type"]);
    switch (type) {
        case 'circle':
            return <iconGraphCircle_1.IconGraphCircle {...props} ref={ref}/>;
        case 'bar':
            return <iconGraphBar_1.IconGraphBar {...props} ref={ref}/>;
        default:
            return <iconGraphLine_1.IconGraphLine {...props} ref={ref}/>;
    }
});
exports.IconGraph = IconGraph;
IconGraph.displayName = 'IconGraph';
//# sourceMappingURL=iconGraph.jsx.map