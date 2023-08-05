Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var cloneDeep_1 = tslib_1.__importDefault(require("lodash/cloneDeep"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var dashboards_1 = require("app/actionCreators/dashboards");
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var widgetQueriesForm_1 = tslib_1.__importDefault(require("app/components/dashboards/widgetQueriesForm"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var fields_1 = require("app/utils/discover/fields");
var measurements_1 = tslib_1.__importDefault(require("app/utils/measurements/measurements"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withTags_1 = tslib_1.__importDefault(require("app/utils/withTags"));
var data_1 = require("app/views/dashboardsV2/data");
var types_1 = require("app/views/dashboardsV2/types");
var widgetCard_1 = tslib_1.__importDefault(require("app/views/dashboardsV2/widgetCard"));
var utils_1 = require("app/views/eventsV2/utils");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var newQuery = {
    name: '',
    fields: ['count()'],
    conditions: '',
    orderby: '',
};
function mapErrors(data, update) {
    Object.keys(data).forEach(function (key) {
        var value = data[key];
        // Recurse into nested objects.
        if (Array.isArray(value) && typeof value[0] === 'string') {
            update[key] = value[0];
        }
        else if (Array.isArray(value) && typeof value[0] === 'object') {
            update[key] = value.map(function (item) { return mapErrors(item, {}); });
        }
        else {
            update[key] = mapErrors(value, {});
        }
    });
    return update;
}
function normalizeQueries(displayType, queries) {
    var e_1, _a, e_2, _b;
    var isTimeseriesChart = ['line', 'area', 'stacked_area', 'bar'].includes(displayType);
    if (['table', 'world_map', 'big_number'].includes(displayType)) {
        // Some display types may only support at most 1 query.
        queries = queries.slice(0, 1);
    }
    else if (isTimeseriesChart) {
        // Timeseries charts supports at most 3 queries.
        queries = queries.slice(0, 3);
    }
    if (displayType === 'table') {
        return queries;
    }
    // Filter out non-aggregate fields
    queries = queries.map(function (query) {
        var fields = query.fields.filter(fields_1.isAggregateField);
        if (isTimeseriesChart || displayType === 'world_map') {
            // Filter out fields that will not generate numeric output types
            fields = fields.filter(function (field) { return fields_1.isLegalYAxisType(fields_1.aggregateOutputType(field)); });
        }
        if (isTimeseriesChart && fields.length && fields.length > 3) {
            // Timeseries charts supports at most 3 fields.
            fields = fields.slice(0, 3);
        }
        return tslib_1.__assign(tslib_1.__assign({}, query), { fields: fields.length ? fields : ['count()'] });
    });
    if (isTimeseriesChart) {
        // For timeseries widget, all queries must share identical set of fields.
        var referenceFields_1 = tslib_1.__spreadArray([], tslib_1.__read(queries[0].fields));
        try {
            queryLoop: for (var queries_1 = tslib_1.__values(queries), queries_1_1 = queries_1.next(); !queries_1_1.done; queries_1_1 = queries_1.next()) {
                var query = queries_1_1.value;
                if (referenceFields_1.length >= 3) {
                    break;
                }
                if (isEqual_1.default(referenceFields_1, query.fields)) {
                    continue;
                }
                try {
                    for (var _c = (e_2 = void 0, tslib_1.__values(query.fields)), _d = _c.next(); !_d.done; _d = _c.next()) {
                        var field = _d.value;
                        if (referenceFields_1.length >= 3) {
                            break queryLoop;
                        }
                        if (!referenceFields_1.includes(field)) {
                            referenceFields_1.push(field);
                        }
                    }
                }
                catch (e_2_1) { e_2 = { error: e_2_1 }; }
                finally {
                    try {
                        if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
                    }
                    finally { if (e_2) throw e_2.error; }
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (queries_1_1 && !queries_1_1.done && (_a = queries_1.return)) _a.call(queries_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        queries = queries.map(function (query) {
            return tslib_1.__assign(tslib_1.__assign({}, query), { fields: referenceFields_1 });
        });
    }
    if (['world_map', 'big_number'].includes(displayType)) {
        // For world map chart, cap fields of the queries to only one field.
        queries = queries.map(function (query) {
            return tslib_1.__assign(tslib_1.__assign({}, query), { fields: query.fields.slice(0, 1) });
        });
    }
    return queries;
}
var AddDashboardWidgetModal = /** @class */ (function (_super) {
    tslib_1.__extends(AddDashboardWidgetModal, _super);
    function AddDashboardWidgetModal(props) {
        var _this = _super.call(this, props) || this;
        _this.handleSubmit = function (event) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, closeModal, organization, onAddWidget, onUpdateWidget, previousWidget, widgetData, err_1, errors;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        event.preventDefault();
                        _a = this.props, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, onAddWidget = _a.onAddWidget, onUpdateWidget = _a.onUpdateWidget, previousWidget = _a.widget;
                        this.setState({ loading: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, 4, 5]);
                        widgetData = pick_1.default(this.state, [
                            'title',
                            'displayType',
                            'interval',
                            'queries',
                        ]);
                        return [4 /*yield*/, dashboards_1.validateWidget(api, organization.slug, widgetData)];
                    case 2:
                        _c.sent();
                        if (typeof onUpdateWidget === 'function' && !!previousWidget) {
                            onUpdateWidget(tslib_1.__assign({ id: previousWidget === null || previousWidget === void 0 ? void 0 : previousWidget.id }, widgetData));
                            indicator_1.addSuccessMessage(locale_1.t('Updated widget.'));
                        }
                        else {
                            onAddWidget(widgetData);
                            indicator_1.addSuccessMessage(locale_1.t('Added widget.'));
                        }
                        closeModal();
                        return [3 /*break*/, 5];
                    case 3:
                        err_1 = _c.sent();
                        errors = mapErrors((_b = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) !== null && _b !== void 0 ? _b : {}, {});
                        this.setState({ errors: errors });
                        return [3 /*break*/, 5];
                    case 4:
                        this.setState({ loading: false });
                        return [7 /*endfinally*/];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        _this.handleFieldChange = function (field) { return function (value) {
            _this.setState(function (prevState) {
                var newState = cloneDeep_1.default(prevState);
                set_1.default(newState, field, value);
                if (field === 'displayType') {
                    var displayType = value;
                    set_1.default(newState, 'queries', normalizeQueries(displayType, prevState.queries));
                }
                return tslib_1.__assign(tslib_1.__assign({}, newState), { errors: undefined });
            });
        }; };
        _this.handleQueryChange = function (widgetQuery, index) {
            _this.setState(function (prevState) {
                var newState = cloneDeep_1.default(prevState);
                set_1.default(newState, "queries." + index, widgetQuery);
                return tslib_1.__assign(tslib_1.__assign({}, newState), { errors: undefined });
            });
        };
        _this.handleQueryRemove = function (index) {
            _this.setState(function (prevState) {
                var newState = cloneDeep_1.default(prevState);
                newState.queries.splice(index, 1);
                return tslib_1.__assign(tslib_1.__assign({}, newState), { errors: undefined });
            });
        };
        _this.handleAddSearchConditions = function () {
            _this.setState(function (prevState) {
                var newState = cloneDeep_1.default(prevState);
                newState.queries.push(cloneDeep_1.default(newQuery));
                return newState;
            });
        };
        var widget = props.widget;
        if (!widget) {
            _this.state = {
                title: '',
                displayType: types_1.DisplayType.LINE,
                interval: '5m',
                queries: [tslib_1.__assign({}, newQuery)],
                errors: undefined,
                loading: false,
            };
            return _this;
        }
        _this.state = {
            title: widget.title,
            displayType: widget.displayType,
            interval: widget.interval,
            queries: normalizeQueries(widget.displayType, widget.queries),
            errors: undefined,
            loading: false,
        };
        return _this;
    }
    AddDashboardWidgetModal.prototype.canAddSearchConditions = function () {
        var rightDisplayType = ['line', 'area', 'stacked_area', 'bar'].includes(this.state.displayType);
        var underQueryLimit = this.state.queries.length < 3;
        return rightDisplayType && underQueryLimit;
    };
    AddDashboardWidgetModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Footer = _a.Footer, Body = _a.Body, Header = _a.Header, api = _a.api, organization = _a.organization, selection = _a.selection, tags = _a.tags, onUpdateWidget = _a.onUpdateWidget, previousWidget = _a.widget;
        var state = this.state;
        var errors = state.errors;
        var fieldOptions = function (measurementKeys) {
            return utils_1.generateFieldOptions({
                organization: organization,
                tagKeys: Object.values(tags).map(function (_a) {
                    var key = _a.key;
                    return key;
                }),
                measurementKeys: measurementKeys,
            });
        };
        var isUpdatingWidget = typeof onUpdateWidget === 'function' && !!previousWidget;
        return (<React.Fragment>
        <Header closeButton>
          <h4>{isUpdatingWidget ? locale_1.t('Edit Widget') : locale_1.t('Add Widget')}</h4>
        </Header>
        <Body>
          <DoubleFieldWrapper>
            <field_1.default data-test-id="widget-name" label={locale_1.t('Widget Name')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.title} required>
              <input_1.default type="text" name="title" maxLength={255} required value={state.title} onChange={function (event) {
                _this.handleFieldChange('title')(event.target.value);
            }}/>
            </field_1.default>
            <field_1.default data-test-id="chart-type" label={locale_1.t('Visualization Display')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.displayType} required>
              <selectControl_1.default required options={data_1.DISPLAY_TYPE_CHOICES.slice()} name="displayType" label={locale_1.t('Visualization Display')} value={state.displayType} onChange={function (option) {
                _this.handleFieldChange('displayType')(option.value);
            }}/>
            </field_1.default>
          </DoubleFieldWrapper>
          <measurements_1.default organization={organization}>
            {function (_a) {
                var measurements = _a.measurements;
                var measurementKeys = Object.values(measurements).map(function (_a) {
                    var key = _a.key;
                    return key;
                });
                var amendedFieldOptions = fieldOptions(measurementKeys);
                return (<widgetQueriesForm_1.default organization={organization} selection={selection} fieldOptions={amendedFieldOptions} displayType={state.displayType} queries={state.queries} errors={errors === null || errors === void 0 ? void 0 : errors.queries} onChange={function (queryIndex, widgetQuery) {
                        return _this.handleQueryChange(widgetQuery, queryIndex);
                    }} canAddSearchConditions={_this.canAddSearchConditions()} handleAddSearchConditions={_this.handleAddSearchConditions} handleDeleteQuery={_this.handleQueryRemove}/>);
            }}
          </measurements_1.default>
          <widgetCard_1.default api={api} organization={organization} selection={selection} widget={this.state} isEditing={false} onDelete={function () { return undefined; }} onEdit={function () { return undefined; }} renderErrorMessage={function (errorMessage) {
                return typeof errorMessage === 'string' && (<panels_1.PanelAlert type="error">{errorMessage}</panels_1.PanelAlert>);
            }} isSorting={false} currentWidgetDragging={false}/>
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default external href="https://docs.sentry.io/product/dashboards/custom-dashboards/#widget-builder">
              {locale_1.t('Read the docs')}
            </button_1.default>
            <button_1.default data-test-id="add-widget" priority="primary" type="button" onClick={this.handleSubmit} disabled={state.loading} busy={state.loading}>
              {isUpdatingWidget ? locale_1.t('Update Widget') : locale_1.t('Add Widget')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </React.Fragment>);
    };
    return AddDashboardWidgetModal;
}(React.Component));
var DoubleFieldWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-column-gap: ", ";\n  width: 100%;\n"], ["\n  display: inline-grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-column-gap: ", ";\n  width: 100%;\n"])), space_1.default(1));
exports.modalCss = react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  max-width: 700px;\n  margin: 70px auto;\n"], ["\n  width: 100%;\n  max-width: 700px;\n  margin: 70px auto;\n"])));
exports.default = withApi_1.default(withGlobalSelection_1.default(withTags_1.default(AddDashboardWidgetModal)));
var templateObject_1, templateObject_2;
//# sourceMappingURL=addDashboardWidgetModal.jsx.map