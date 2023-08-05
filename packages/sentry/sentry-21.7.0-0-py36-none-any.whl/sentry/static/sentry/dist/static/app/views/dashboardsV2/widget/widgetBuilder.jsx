Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var utils_1 = require("app/utils");
var eventWidget_1 = tslib_1.__importDefault(require("./eventWidget"));
var metricWidget_1 = tslib_1.__importDefault(require("./metricWidget"));
var utils_2 = require("./utils");
function WidgetBuilder(_a) {
    var dashboard = _a.dashboard, onSave = _a.onSave, widget = _a.widget, params = _a.params, location = _a.location, router = _a.router, organization = _a.organization;
    var _b = tslib_1.__read(react_1.useState(utils_2.DataSet.EVENTS), 2), dataSet = _b[0], setDataSet = _b[1];
    var isEditing = !!widget;
    var widgetId = params.widgetId, orgId = params.orgId, dashboardId = params.dashboardId;
    var goBackLocation = {
        pathname: dashboardId
            ? "/organizations/" + orgId + "/dashboard/" + dashboardId + "/"
            : "/organizations/" + orgId + "/dashboards/new/",
        query: tslib_1.__assign(tslib_1.__assign({}, location.query), { dataSet: undefined }),
    };
    react_1.useEffect(function () {
        checkDataSet();
    });
    function checkDataSet() {
        var query = location.query;
        var queryDataSet = query === null || query === void 0 ? void 0 : query.dataSet;
        if (!queryDataSet) {
            router.replace({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { dataSet: utils_2.DataSet.EVENTS }),
            });
            return;
        }
        if (queryDataSet !== utils_2.DataSet.EVENTS && queryDataSet !== utils_2.DataSet.METRICS) {
            setDataSet(undefined);
            return;
        }
        if (queryDataSet === utils_2.DataSet.METRICS) {
            if (dataSet === utils_2.DataSet.METRICS) {
                return;
            }
            setDataSet(utils_2.DataSet.METRICS);
            return;
        }
        if (dataSet === utils_2.DataSet.EVENTS) {
            return;
        }
        setDataSet(utils_2.DataSet.EVENTS);
    }
    function handleDataSetChange(newDataSet) {
        router.replace({
            pathname: location.pathname,
            query: tslib_1.__assign(tslib_1.__assign({}, location.query), { dataSet: newDataSet }),
        });
    }
    if (!dataSet) {
        return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
        {locale_1.t('Data set not found.')}
      </alert_1.default>);
    }
    function handleAddWidget(newWidget) {
        onSave(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(dashboard.widgets)), [newWidget]));
    }
    if ((isEditing && !utils_1.defined(widgetId)) ||
        (isEditing && utils_1.defined(widgetId) && !dashboard.widgets[widgetId])) {
        return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
        {locale_1.t('Widget not found.')}
      </alert_1.default>);
    }
    function handleUpdateWidget(nextWidget) {
        if (!widgetId) {
            return;
        }
        var nextList = tslib_1.__spreadArray([], tslib_1.__read(dashboard.widgets));
        nextList[widgetId] = nextWidget;
        onSave(nextList);
    }
    function handleDeleteWidget() {
        if (!widgetId) {
            return;
        }
        var nextList = tslib_1.__spreadArray([], tslib_1.__read(dashboard.widgets));
        nextList.splice(widgetId, 1);
        onSave(nextList);
    }
    if (dataSet === utils_2.DataSet.EVENTS) {
        return (<eventWidget_1.default dashboardTitle={dashboard.title} widget={widget} onAdd={handleAddWidget} onUpdate={handleUpdateWidget} onDelete={handleDeleteWidget} onChangeDataSet={handleDataSetChange} goBackLocation={goBackLocation} isEditing={isEditing}/>);
    }
    return (<metricWidget_1.default organization={organization} router={router} location={location} dashboardTitle={dashboard.title} params={params} goBackLocation={goBackLocation} onChangeDataSet={handleDataSetChange}/>);
}
exports.default = WidgetBuilder;
//# sourceMappingURL=widgetBuilder.jsx.map