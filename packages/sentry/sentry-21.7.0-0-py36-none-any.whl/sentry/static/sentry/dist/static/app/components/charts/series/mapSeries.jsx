Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("echarts/lib/chart/map");
function MapSeries(props) {
    if (props === void 0) { props = {}; }
    return tslib_1.__assign(tslib_1.__assign({ roam: true, itemStyle: {
            // TODO(ts): label doesn't seem to exist on the emphasis? I have not
            //           verified if removing this has an affect on the world chart.
            emphasis: { label: { show: false } },
        } }, props), { type: 'map' });
}
exports.default = MapSeries;
//# sourceMappingURL=mapSeries.jsx.map