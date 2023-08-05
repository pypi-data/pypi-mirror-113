var _a;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var environment_1 = require("app/utils/environment");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var utils_1 = require("app/views/alerts/utils");
var options_1 = require("app/views/alerts/wizard/options");
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var constants_1 = require("./constants");
var metricField_1 = tslib_1.__importDefault(require("./metricField"));
var types_1 = require("./types");
var TIME_WINDOW_MAP = (_a = {},
    _a[types_1.TimeWindow.ONE_MINUTE] = locale_1.t('1 minute'),
    _a[types_1.TimeWindow.FIVE_MINUTES] = locale_1.t('5 minutes'),
    _a[types_1.TimeWindow.TEN_MINUTES] = locale_1.t('10 minutes'),
    _a[types_1.TimeWindow.FIFTEEN_MINUTES] = locale_1.t('15 minutes'),
    _a[types_1.TimeWindow.THIRTY_MINUTES] = locale_1.t('30 minutes'),
    _a[types_1.TimeWindow.ONE_HOUR] = locale_1.t('1 hour'),
    _a[types_1.TimeWindow.TWO_HOURS] = locale_1.t('2 hours'),
    _a[types_1.TimeWindow.FOUR_HOURS] = locale_1.t('4 hours'),
    _a[types_1.TimeWindow.ONE_DAY] = locale_1.t('24 hours'),
    _a);
var RuleConditionsFormForWizard = /** @class */ (function (_super) {
    tslib_1.__extends(RuleConditionsFormForWizard, _super);
    function RuleConditionsFormForWizard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            environments: null,
        };
        return _this;
    }
    RuleConditionsFormForWizard.prototype.componentDidMount = function () {
        this.fetchData();
    };
    RuleConditionsFormForWizard.prototype.fetchData = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, api, organization, projectSlug, environments, _err_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/environments/", {
                                query: {
                                    visibility: 'visible',
                                },
                            })];
                    case 2:
                        environments = _b.sent();
                        this.setState({ environments: environments });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to fetch environments'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    RuleConditionsFormForWizard.prototype.render = function () {
        var _a;
        var _b = this.props, organization = _b.organization, disabled = _b.disabled, onFilterSearch = _b.onFilterSearch, allowChangeEventTypes = _b.allowChangeEventTypes, alertType = _b.alertType;
        var environments = this.state.environments;
        var environmentOptions = (_a = environments === null || environments === void 0 ? void 0 : environments.map(function (env) { return ({
            value: env.name,
            label: environment_1.getDisplayName(env),
        }); })) !== null && _a !== void 0 ? _a : [];
        var anyEnvironmentLabel = (<React.Fragment>
        {locale_1.t('All')}
        <div className="all-environment-note">
          {locale_1.tct("This will count events across every environment. For example,\n             having 50 [code1:production] events and 50 [code2:development]\n             events would trigger an alert with a critical threshold of 100.", { code1: <code />, code2: <code /> })}
        </div>
      </React.Fragment>);
        environmentOptions.unshift({ value: null, label: anyEnvironmentLabel });
        var dataSourceOptions = [
            {
                label: locale_1.t('Errors'),
                options: [
                    {
                        value: types_1.Datasource.ERROR_DEFAULT,
                        label: utils_1.DATA_SOURCE_LABELS[types_1.Datasource.ERROR_DEFAULT],
                    },
                    {
                        value: types_1.Datasource.DEFAULT,
                        label: utils_1.DATA_SOURCE_LABELS[types_1.Datasource.DEFAULT],
                    },
                    {
                        value: types_1.Datasource.ERROR,
                        label: utils_1.DATA_SOURCE_LABELS[types_1.Datasource.ERROR],
                    },
                ],
            },
        ];
        if (organization.features.includes('performance-view') && alertType === 'custom') {
            dataSourceOptions.push({
                label: locale_1.t('Transactions'),
                options: [
                    {
                        value: types_1.Datasource.TRANSACTION,
                        label: utils_1.DATA_SOURCE_LABELS[types_1.Datasource.TRANSACTION],
                    },
                ],
            });
        }
        var formElemBaseStyle = {
            padding: "" + space_1.default(0.5),
            border: 'none',
        };
        var _c = options_1.getFunctionHelpText(alertType), intervalLabelText = _c.labelText, timeWindowText = _c.timeWindowText;
        return (<React.Fragment>
        <ChartPanel>
          <StyledPanelBody>{this.props.thresholdChart}</StyledPanelBody>
        </ChartPanel>
        <StyledListItem>{locale_1.t('Filter events')}</StyledListItem>
        <FormRow>
          <selectField_1.default name="environment" placeholder={locale_1.t('All')} style={tslib_1.__assign(tslib_1.__assign({}, formElemBaseStyle), { minWidth: 180, flex: 1 })} styles={{
                singleValue: function (base) { return (tslib_1.__assign(tslib_1.__assign({}, base), { '.all-environment-note': { display: 'none' } })); },
                option: function (base, state) { return (tslib_1.__assign(tslib_1.__assign({}, base), { '.all-environment-note': tslib_1.__assign(tslib_1.__assign({}, (!state.isSelected && !state.isFocused
                        ? { color: theme_1.default.gray400 }
                        : {})), { fontSize: theme_1.default.fontSizeSmall }) })); },
            }} options={environmentOptions} isDisabled={disabled || this.state.environments === null} isClearable inline={false} flexibleControlStateSize inFieldLabel={locale_1.t('Env: ')}/>
          {allowChangeEventTypes && (<formField_1.default name="datasource" inline={false} style={tslib_1.__assign(tslib_1.__assign({}, formElemBaseStyle), { minWidth: 300, flex: 2 })} flexibleControlStateSize>
              {function (_a) {
                    var onChange = _a.onChange, onBlur = _a.onBlur, model = _a.model;
                    var formDataset = model.getValue('dataset');
                    var formEventTypes = model.getValue('eventTypes');
                    var mappedValue = utils_1.convertDatasetEventTypesToSource(formDataset, formEventTypes);
                    return (<selectControl_1.default value={mappedValue} inFieldLabel={locale_1.t('Events: ')} onChange={function (optionObj) {
                            var _a;
                            var optionValue = optionObj.value;
                            onChange(optionValue, {});
                            onBlur(optionValue, {});
                            // Reset the aggregate to the default (which works across
                            // datatypes), otherwise we may send snuba an invalid query
                            // (transaction aggregate on events datasource = bad).
                            optionValue === 'transaction'
                                ? model.setValue('aggregate', constants_1.DEFAULT_TRANSACTION_AGGREGATE)
                                : model.setValue('aggregate', constants_1.DEFAULT_AGGREGATE);
                            // set the value of the dataset and event type from data source
                            var _b = (_a = utils_1.DATA_SOURCE_TO_SET_AND_EVENT_TYPES[optionValue]) !== null && _a !== void 0 ? _a : {}, dataset = _b.dataset, eventTypes = _b.eventTypes;
                            model.setValue('dataset', dataset);
                            model.setValue('eventTypes', eventTypes);
                        }} options={dataSourceOptions} isDisabled={disabled} required/>);
                }}
            </formField_1.default>)}
          <formField_1.default name="query" inline={false} style={tslib_1.__assign(tslib_1.__assign({}, formElemBaseStyle), { flex: '6 0 500px' })} flexibleControlStateSize>
            {function (_a) {
                var _b;
                var onChange = _a.onChange, onBlur = _a.onBlur, onKeyDown = _a.onKeyDown, initialData = _a.initialData, model = _a.model;
                return (<SearchContainer>
                <StyledSearchBar searchSource="alert_builder" defaultQuery={(_b = initialData === null || initialData === void 0 ? void 0 : initialData.query) !== null && _b !== void 0 ? _b : ''} omitTags={['event.type']} disabled={disabled} useFormWrapper={false} organization={organization} placeholder={model.getValue('dataset') === 'events'
                        ? locale_1.t('Filter events by level, message, or other properties...')
                        : locale_1.t('Filter transactions by URL, tags, and other properties...')} onChange={onChange} onKeyDown={function (e) {
                        /**
                         * Do not allow enter key to submit the alerts form since it is unlikely
                         * users will be ready to create the rule as this sits above required fields.
                         */
                        if (e.key === 'Enter') {
                            e.preventDefault();
                            e.stopPropagation();
                        }
                        onKeyDown === null || onKeyDown === void 0 ? void 0 : onKeyDown(e);
                    }} onBlur={function (query) {
                        onFilterSearch(query);
                        onBlur(query);
                    }} onSearch={function (query) {
                        onFilterSearch(query);
                        onChange(query, {});
                    }}/>
              </SearchContainer>);
            }}
          </formField_1.default>
        </FormRow>
        <StyledListItem>
          <StyledListTitle>
            <div>{intervalLabelText}</div>
            <tooltip_1.default title={locale_1.t('Time window over which the metric is evaluated. Alerts are evaluated every minute regardless of this value.')}>
              <icons_1.IconQuestion size="sm" color="gray200"/>
            </tooltip_1.default>
          </StyledListTitle>
        </StyledListItem>
        <FormRow>
          {timeWindowText && (<metricField_1.default name="aggregate" help={null} organization={organization} disabled={disabled} style={tslib_1.__assign({}, formElemBaseStyle)} inline={false} flexibleControlStateSize columnWidth={200} alertType={alertType} required/>)}
          {timeWindowText && <FormRowText>{timeWindowText}</FormRowText>}
          <selectField_1.default name="timeWindow" style={tslib_1.__assign(tslib_1.__assign({}, formElemBaseStyle), { flex: '0 150px 0', minWidth: 130, maxWidth: 300 })} choices={Object.entries(TIME_WINDOW_MAP)} required isDisabled={disabled} getValue={function (value) { return Number(value); }} setValue={function (value) { return "" + value; }} inline={false} flexibleControlStateSize/>
        </FormRow>
      </React.Fragment>);
    };
    return RuleConditionsFormForWizard;
}(React.PureComponent));
var StyledListTitle = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  span {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  span {\n    margin-left: ", ";\n  }\n"])), space_1.default(1));
var ChartPanel = styled_1.default(panels_1.Panel)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(4));
var StyledPanelBody = styled_1.default(panels_1.PanelBody)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ol,\n  h4 {\n    margin-bottom: ", ";\n  }\n"], ["\n  ol,\n  h4 {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(1));
var SearchContainer = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledListItem = styled_1.default(listItem_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  font-size: ", ";\n  line-height: 1.3;\n"], ["\n  margin-bottom: ", ";\n  font-size: ", ";\n  line-height: 1.3;\n"])), space_1.default(1), function (p) { return p.theme.fontSizeExtraLarge; });
var FormRow = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  flex-wrap: wrap;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n  flex-wrap: wrap;\n  margin-bottom: ", ";\n"])), space_1.default(4));
var FormRowText = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space_1.default(1));
exports.default = RuleConditionsFormForWizard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=ruleConditionsFormForWizard.jsx.map