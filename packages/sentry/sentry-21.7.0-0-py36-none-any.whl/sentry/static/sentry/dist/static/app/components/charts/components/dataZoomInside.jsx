Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("echarts/lib/component/dataZoomInside");
var DEFAULT = {
    type: 'inside',
    zoomOnMouseWheel: 'shift',
    throttle: 50,
};
function DataZoomInside(props) {
    // `props` can be boolean, if so return default
    if (!props || !Array.isArray(props)) {
        var dataZoom = tslib_1.__assign(tslib_1.__assign({}, DEFAULT), props);
        return [dataZoom];
    }
    return props;
}
exports.default = DataZoomInside;
//# sourceMappingURL=dataZoomInside.jsx.map