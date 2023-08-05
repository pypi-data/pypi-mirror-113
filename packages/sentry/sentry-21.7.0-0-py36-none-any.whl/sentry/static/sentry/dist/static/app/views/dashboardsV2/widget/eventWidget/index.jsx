Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var cloneDeep_1 = tslib_1.__importDefault(require("lodash/cloneDeep"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var dashboards_1 = require("app/actionCreators/dashboards");
var indicator_1 = require("app/actionCreators/indicator");
var widgetQueryFields_1 = tslib_1.__importDefault(require("app/components/dashboards/widgetQueryFields"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var measurements_1 = tslib_1.__importDefault(require("app/utils/measurements/measurements"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withTags_1 = tslib_1.__importDefault(require("app/utils/withTags"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var widgetCard_1 = tslib_1.__importDefault(require("app/views/dashboardsV2/widgetCard"));
var utils_2 = require("app/views/eventsV2/utils");
var types_1 = require("../../types");
var buildStep_1 = tslib_1.__importDefault(require("../buildStep"));
var buildSteps_1 = tslib_1.__importDefault(require("../buildSteps"));
var choseDataStep_1 = tslib_1.__importDefault(require("../choseDataStep"));
var header_1 = tslib_1.__importDefault(require("../header"));
var utils_3 = require("../utils");
var queries_1 = tslib_1.__importDefault(require("./queries"));
var utils_4 = require("./utils");
var newQuery = {
    name: '',
    fields: ['count()'],
    conditions: '',
    orderby: '',
};
var EventWidget = /** @class */ (function (_super) {
    tslib_1.__extends(EventWidget, _super);
    function EventWidget() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFieldChange = function (field, value) {
            _this.setState(function (state) {
                var newState = cloneDeep_1.default(state);
                if (field === 'displayType') {
                    set_1.default(newState, 'queries', utils_4.normalizeQueries(value, state.queries));
                    if (state.title === locale_1.t('Custom %s Widget', state.displayType) ||
                        state.title === locale_1.t('Custom %s Widget', types_1.DisplayType.AREA)) {
                        return tslib_1.__assign(tslib_1.__assign({}, newState), { title: locale_1.t('Custom %s Widget', utils_3.displayTypes[value]), widgetErrors: undefined });
                    }
                    set_1.default(newState, field, value);
                }
                return tslib_1.__assign(tslib_1.__assign({}, newState), { widgetErrors: undefined });
            });
        };
        _this.handleRemoveQuery = function (index) {
            _this.setState(function (state) {
                var newState = cloneDeep_1.default(state);
                newState.queries.splice(index, 1);
                return tslib_1.__assign(tslib_1.__assign({}, newState), { widgetErrors: undefined });
            });
        };
        _this.handleAddQuery = function () {
            _this.setState(function (state) {
                var newState = cloneDeep_1.default(state);
                newState.queries.push(cloneDeep_1.default(newQuery));
                return newState;
            });
        };
        _this.handleChangeQuery = function (index, query) {
            _this.setState(function (state) {
                var newState = cloneDeep_1.default(state);
                set_1.default(newState, "queries." + index, query);
                return tslib_1.__assign(tslib_1.__assign({}, newState), { widgetErrors: undefined });
            });
        };
        _this.handleSave = function (event) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, organization, onAdd, isEditing, onUpdate, widget, widgetData, err_1, widgetErrors;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        event.preventDefault();
                        this.setState({ loading: true });
                        _a = this.props, organization = _a.organization, onAdd = _a.onAdd, isEditing = _a.isEditing, onUpdate = _a.onUpdate, widget = _a.widget;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, 4, 5]);
                        widgetData = pick_1.default(this.state, [
                            'title',
                            'displayType',
                            'interval',
                            'queries',
                        ]);
                        return [4 /*yield*/, dashboards_1.validateWidget(this.api, organization.slug, widgetData)];
                    case 2:
                        _c.sent();
                        if (isEditing) {
                            onUpdate(tslib_1.__assign({ id: widget.id }, widgetData));
                            indicator_1.addSuccessMessage(locale_1.t('Updated widget'));
                            return [2 /*return*/];
                        }
                        onAdd(widgetData);
                        indicator_1.addSuccessMessage(locale_1.t('Added widget'));
                        return [3 /*break*/, 5];
                    case 3:
                        err_1 = _c.sent();
                        widgetErrors = utils_4.mapErrors((_b = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) !== null && _b !== void 0 ? _b : {}, {});
                        this.setState({ widgetErrors: widgetErrors });
                        return [3 /*break*/, 5];
                    case 4:
                        this.setState({ loading: false });
                        return [7 /*endfinally*/];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    EventWidget.prototype.getDefaultState = function () {
        var widget = this.props.widget;
        if (!widget) {
            return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { title: locale_1.t('Custom %s Widget', utils_3.displayTypes[types_1.DisplayType.AREA]), displayType: types_1.DisplayType.AREA, interval: '5m', queries: [tslib_1.__assign({}, newQuery)] });
        }
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { title: widget.title, displayType: widget.displayType, interval: widget.interval, queries: utils_4.normalizeQueries(widget.displayType, widget.queries), widgetErrors: undefined });
    };
    EventWidget.prototype.getFirstQueryError = function (field) {
        var _a;
        var _b;
        var widgetErrors = this.state.widgetErrors;
        if (!widgetErrors) {
            return undefined;
        }
        var _c = tslib_1.__read((_b = Object.entries(widgetErrors).find(function (widgetErrorKey, _) { return String(widgetErrorKey) === field; })) !== null && _b !== void 0 ? _b : [], 2), key = _c[0], value = _c[1];
        if (utils_1.defined(key) && utils_1.defined(value)) {
            return _a = {}, _a[key] = value, _a;
        }
        return undefined;
    };
    EventWidget.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, onChangeDataSet = _a.onChangeDataSet, selection = _a.selection, tags = _a.tags, isEditing = _a.isEditing, goBackLocation = _a.goBackLocation, dashboardTitle = _a.dashboardTitle, onDelete = _a.onDelete;
        var _b = this.state, title = _b.title, displayType = _b.displayType, queries = _b.queries, interval = _b.interval, widgetErrors = _b.widgetErrors;
        var orgSlug = organization.slug;
        function fieldOptions(measurementKeys) {
            return utils_2.generateFieldOptions({
                organization: organization,
                tagKeys: Object.values(tags).map(function (_a) {
                    var key = _a.key;
                    return key;
                }),
                measurementKeys: measurementKeys,
            });
        }
        return (<StyledPageContent>
        <header_1.default dashboardTitle={dashboardTitle} orgSlug={orgSlug} title={title} isEditing={isEditing} onChangeTitle={function (newTitle) { return _this.handleFieldChange('title', newTitle); }} onSave={this.handleSave} onDelete={onDelete} goBackLocation={goBackLocation}/>
        <Layout.Body>
          <buildSteps_1.default>
            <buildStep_1.default title={locale_1.t('Choose your visualization')} description={locale_1.t('This is a preview of how your widget will appear in the dashboard.')}>
              <VisualizationWrapper>
                <selectControl_1.default name="displayType" options={Object.keys(utils_3.displayTypes).map(function (value) { return ({
                label: utils_3.displayTypes[value],
                value: value,
            }); })} value={displayType} onChange={function (option) {
                _this.handleFieldChange('displayType', option.value);
            }} error={widgetErrors === null || widgetErrors === void 0 ? void 0 : widgetErrors.displayType}/>
                <widgetCard_1.default api={this.api} organization={organization} selection={selection} widget={{ title: title, queries: queries, displayType: displayType, interval: interval }} isEditing={false} onDelete={function () { return undefined; }} onEdit={function () { return undefined; }} renderErrorMessage={function (errorMessage) {
                return typeof errorMessage === 'string' && (<panels_1.PanelAlert type="error">{errorMessage}</panels_1.PanelAlert>);
            }} isSorting={false} currentWidgetDragging={false}/>
              </VisualizationWrapper>
            </buildStep_1.default>
            <choseDataStep_1.default value={utils_3.DataSet.EVENTS} onChange={onChangeDataSet}/>
            <buildStep_1.default title={locale_1.t('Begin your search')} description={locale_1.t('Add another query to compare projects, tags, etc.')}>
              <queries_1.default queries={queries} selectedProjectIds={selection.projects} organization={organization} displayType={displayType} onRemoveQuery={this.handleRemoveQuery} onAddQuery={this.handleAddQuery} onChangeQuery={this.handleChangeQuery} errors={widgetErrors === null || widgetErrors === void 0 ? void 0 : widgetErrors.queries}/>
            </buildStep_1.default>
            <measurements_1.default organization={organization}>
              {function (_a) {
                var measurements = _a.measurements;
                var measurementKeys = Object.values(measurements).map(function (_a) {
                    var key = _a.key;
                    return key;
                });
                var amendedFieldOptions = fieldOptions(measurementKeys);
                var buildStepContent = (<widgetQueryFields_1.default style={{ padding: 0 }} errors={_this.getFirstQueryError('fields')} displayType={displayType} fieldOptions={amendedFieldOptions} fields={queries[0].fields} organization={organization} onChange={function (fields) {
                        queries.forEach(function (query, queryIndex) {
                            var clonedQuery = cloneDeep_1.default(query);
                            clonedQuery.fields = fields;
                            _this.handleChangeQuery(queryIndex, clonedQuery);
                        });
                    }}/>);
                return (<buildStep_1.default title={displayType === types_1.DisplayType.TABLE
                        ? locale_1.t('Choose your columns')
                        : locale_1.t('Choose your y-axis')} description={locale_1.t('We’ll use this to determine what gets graphed in the y-axis and any additional overlays.')}>
                    {buildStepContent}
                  </buildStep_1.default>);
            }}
            </measurements_1.default>
          </buildSteps_1.default>
        </Layout.Body>
      </StyledPageContent>);
    };
    return EventWidget;
}(asyncView_1.default));
exports.default = withOrganization_1.default(withGlobalSelection_1.default(withTags_1.default(EventWidget)));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var VisualizationWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(1.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map