Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var panels_1 = require("app/components/panels");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var footer_1 = tslib_1.__importDefault(require("../../charts/footer"));
var utils_1 = require("../../utils");
var singleAxisChart_1 = require("./singleAxisChart");
var utils_2 = require("./utils");
function DoubleAxisDisplay(props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, axisOptions = props.axisOptions, leftAxis = props.leftAxis, rightAxis = props.rightAxis;
    var _a = tslib_1.__read(react_1.useState(false), 2), usingBackupAxis = _a[0], setUsingBackupAxis = _a[1];
    var onFilterChange = function (field) { return function (minValue, maxValue) {
        var filterString = utils_1.getTransactionSearchQuery(location);
        var conditions = tokenizeSearch_1.tokenizeSearch(filterString);
        conditions.setTagValues(field, [
            ">=" + Math.round(minValue),
            "<" + Math.round(maxValue),
        ]);
        var query = conditions.formatString();
        analytics_1.trackAnalyticsEvent({
            eventKey: 'performance_views.landingv2.display.filter_change',
            eventName: 'Performance Views: Landing v2 Display Filter Change',
            organization_id: parseInt(organization.id, 10),
            field: field,
            min_value: parseInt(minValue, 10),
            max_value: parseInt(maxValue, 10),
        });
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: tslib_1.__assign(tslib_1.__assign({}, location.query), { query: String(query).trim() }),
        });
    }; };
    var didReceiveMultiAxis = function (useBackup) {
        setUsingBackupAxis(useBackup);
    };
    var leftAxisOrBackup = utils_2.getAxisOrBackupAxis(leftAxis, usingBackupAxis);
    var rightAxisOrBackup = utils_2.getAxisOrBackupAxis(rightAxis, usingBackupAxis);
    var optionsOrBackup = utils_2.getBackupAxes(axisOptions, usingBackupAxis);
    return (<panels_1.Panel>
      <DoubleChartContainer>
        <singleAxisChart_1.SingleAxisChart axis={leftAxis} onFilterChange={onFilterChange(leftAxis.field)} didReceiveMultiAxis={didReceiveMultiAxis} usingBackupAxis={usingBackupAxis} {...props}/>
        <singleAxisChart_1.SingleAxisChart axis={rightAxis} onFilterChange={onFilterChange(rightAxis.field)} didReceiveMultiAxis={didReceiveMultiAxis} usingBackupAxis={usingBackupAxis} {...props}/>
      </DoubleChartContainer>

      <Footer options={optionsOrBackup} leftAxis={leftAxisOrBackup.value} rightAxis={rightAxisOrBackup.value} organization={organization} eventView={eventView} location={location}/>
    </panels_1.Panel>);
}
var DoubleChartContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n  min-height: 282px;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n  min-height: 282px;\n"])), space_1.default(3));
var Footer = withApi_1.default(footer_1.default);
exports.default = DoubleAxisDisplay;
var templateObject_1;
//# sourceMappingURL=doubleAxisDisplay.jsx.map