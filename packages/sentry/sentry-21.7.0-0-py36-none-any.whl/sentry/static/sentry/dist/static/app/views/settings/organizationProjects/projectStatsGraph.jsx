Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_lazyload_1 = tslib_1.__importDefault(require("react-lazyload"));
var miniBarChart_1 = tslib_1.__importDefault(require("app/components/charts/miniBarChart"));
var locale_1 = require("app/locale");
var ProjectStatsGraph = function (_a) {
    var project = _a.project, stats = _a.stats;
    stats = stats || project.stats || [];
    var series = [
        {
            seriesName: locale_1.t('Events'),
            data: stats.map(function (point) { return ({ name: point[0] * 1000, value: point[1] }); }),
        },
    ];
    return (<react_1.Fragment>
      {series && (<react_lazyload_1.default height={25} debounce={50}>
          <miniBarChart_1.default isGroupedByDate showTimeInTooltip series={series} height={25}/>
        </react_lazyload_1.default>)}
    </react_1.Fragment>);
};
exports.default = ProjectStatsGraph;
//# sourceMappingURL=projectStatsGraph.jsx.map