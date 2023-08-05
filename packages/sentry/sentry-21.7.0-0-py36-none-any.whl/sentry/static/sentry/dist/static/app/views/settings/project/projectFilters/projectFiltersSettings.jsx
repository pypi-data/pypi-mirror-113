Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var panels_1 = require("app/components/panels");
var switchButton_1 = tslib_1.__importDefault(require("app/components/switchButton"));
var inboundFilters_1 = tslib_1.__importStar(require("app/data/forms/inboundFilters"));
var locale_1 = require("app/locale");
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var fieldFromConfig_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/fieldFromConfig"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var LEGACY_BROWSER_SUBFILTERS = {
    ie_pre_9: {
        icon: 'internet-explorer',
        helpText: 'Version 8 and lower',
        title: 'Internet Explorer',
    },
    ie9: {
        icon: 'internet-explorer',
        helpText: 'Version 9',
        title: 'Internet Explorer',
    },
    ie10: {
        icon: 'internet-explorer',
        helpText: 'Version 10',
        title: 'Internet Explorer',
    },
    ie11: {
        icon: 'internet-explorer',
        helpText: 'Version 11',
        title: 'Internet Explorer',
    },
    safari_pre_6: {
        icon: 'safari',
        helpText: 'Version 5 and lower',
        title: 'Safari',
    },
    opera_pre_15: {
        icon: 'opera',
        helpText: 'Version 14 and lower',
        title: 'Opera',
    },
    opera_mini_pre_8: {
        icon: 'opera',
        helpText: 'Version 8 and lower',
        title: 'Opera Mini',
    },
    android_pre_4: {
        icon: 'android',
        helpText: 'Version 3 and lower',
        title: 'Android',
    },
};
var LEGACY_BROWSER_KEYS = Object.keys(LEGACY_BROWSER_SUBFILTERS);
var LegacyBrowserFilterRow = /** @class */ (function (_super) {
    tslib_1.__extends(LegacyBrowserFilterRow, _super);
    function LegacyBrowserFilterRow(props) {
        var _this = _super.call(this, props) || this;
        _this.handleToggleSubfilters = function (subfilter, e) {
            var subfilters = _this.state.subfilters;
            if (subfilter === true) {
                subfilters = new Set(LEGACY_BROWSER_KEYS);
            }
            else if (subfilter === false) {
                subfilters = new Set();
            }
            else if (subfilters.has(subfilter)) {
                subfilters.delete(subfilter);
            }
            else {
                subfilters.add(subfilter);
            }
            _this.setState({
                subfilters: new Set(subfilters),
            }, function () {
                _this.props.onToggle(_this.props.data, subfilters, e);
            });
        };
        var initialSubfilters;
        if (props.data.active === true) {
            initialSubfilters = new Set(LEGACY_BROWSER_KEYS);
        }
        else if (props.data.active === false) {
            initialSubfilters = new Set();
        }
        else {
            initialSubfilters = new Set(props.data.active);
        }
        _this.state = {
            loading: false,
            error: false,
            subfilters: initialSubfilters,
        };
        return _this;
    }
    LegacyBrowserFilterRow.prototype.render = function () {
        var _this = this;
        var disabled = this.props.disabled;
        return (<div>
        {!disabled && (<BulkFilter>
            <BulkFilterLabel>{locale_1.t('Filter')}:</BulkFilterLabel>
            <BulkFilterItem onClick={this.handleToggleSubfilters.bind(this, true)}>
              {locale_1.t('All')}
            </BulkFilterItem>
            <BulkFilterItem onClick={this.handleToggleSubfilters.bind(this, false)}>
              {locale_1.t('None')}
            </BulkFilterItem>
          </BulkFilter>)}

        <FilterGrid>
          {LEGACY_BROWSER_KEYS.map(function (key) {
                var subfilter = LEGACY_BROWSER_SUBFILTERS[key];
                return (<FilterGridItemWrapper key={key}>
                <FilterGridItem>
                  <FilterItem>
                    <FilterGridIcon className={"icon-" + subfilter.icon}/>
                    <div>
                      <FilterTitle>{subfilter.title}</FilterTitle>
                      <FilterDescription>{subfilter.helpText}</FilterDescription>
                    </div>
                  </FilterItem>

                  <switchButton_1.default isActive={_this.state.subfilters.has(key)} isDisabled={disabled} css={{ flexShrink: 0, marginLeft: 6 }} toggle={_this.handleToggleSubfilters.bind(_this, key)} size="lg"/>
                </FilterGridItem>
              </FilterGridItemWrapper>);
            })}
        </FilterGrid>
      </div>);
    };
    return LegacyBrowserFilterRow;
}(React.Component));
var ProjectFiltersSettings = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectFiltersSettings, _super);
    function ProjectFiltersSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegacyChange = function (onChange, onBlur, _filter, subfilters, e) {
            onChange === null || onChange === void 0 ? void 0 : onChange(subfilters, e);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(subfilters, e);
        };
        _this.handleSubmit = function (response) {
            // This will update our project context
            projectActions_1.default.updateSuccess(response);
        };
        _this.renderDisabledCustomFilters = function (p) { return (<featureDisabled_1.default featureName={locale_1.t('Custom Inbound Filters')} features={p.features} alert={panels_1.PanelAlert} message={locale_1.t('Release and Error Message filtering are not enabled on your Sentry installation')}/>); };
        _this.renderCustomFilters = function (disabled) { return function () {
            return (<feature_1.default features={['projects:custom-inbound-filters']} hookName="feature-disabled:custom-inbound-filters" renderDisabled={function (_a) {
                    var children = _a.children, props = tslib_1.__rest(_a, ["children"]);
                    if (typeof children === 'function') {
                        return children(tslib_1.__assign(tslib_1.__assign({}, props), { renderDisabled: _this.renderDisabledCustomFilters }));
                    }
                    return null;
                }}>
        {function (_a) {
                    var _b;
                    var hasFeature = _a.hasFeature, organization = _a.organization, renderDisabled = _a.renderDisabled, featureProps = tslib_1.__rest(_a, ["hasFeature", "organization", "renderDisabled"]);
                    return (<React.Fragment>
            {!hasFeature &&
                            typeof renderDisabled === 'function' &&
                            // XXX: children is set to null as we're doing tricksy things
                            // in the renderDisabled prop a few lines higher.
                            renderDisabled(tslib_1.__assign({ organization: organization, hasFeature: hasFeature, children: null }, featureProps))}

            {inboundFilters_1.customFilterFields.map(function (field) { return (<fieldFromConfig_1.default key={field.name} field={field} disabled={disabled || !hasFeature}/>); })}

            {hasFeature && ((_b = _this.props.project.options) === null || _b === void 0 ? void 0 : _b['filters:error_messages']) && (<panels_1.PanelAlert type="warning" data-test-id="error-message-disclaimer">
                {locale_1.t("Minidumps, errors in the minified production build of React, and Internet Explorer's i18n errors cannot be filtered by message.")}
              </panels_1.PanelAlert>)}
          </React.Fragment>);
                }}
      </feature_1.default>);
        }; };
        return _this;
    }
    ProjectFiltersSettings.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { hooksDisabled: hookStore_1.default.get('feature-disabled:custom-inbound-filters') });
    };
    ProjectFiltersSettings.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['filterList', "/projects/" + orgId + "/" + projectId + "/filters/"]];
    };
    ProjectFiltersSettings.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (prevProps.project.slug !== this.props.project.slug) {
            this.reloadData();
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    ProjectFiltersSettings.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, features = _a.features, params = _a.params, project = _a.project;
        var orgId = params.orgId, projectId = params.projectId;
        var projectEndpoint = "/projects/" + orgId + "/" + projectId + "/";
        var filtersEndpoint = projectEndpoint + "filters/";
        return (<access_1.default access={['project:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<React.Fragment>
            <panels_1.Panel>
              <panels_1.PanelHeader>{locale_1.t('Filters')}</panels_1.PanelHeader>
              <panels_1.PanelBody>
                {_this.state.filterList.map(function (filter) {
                        var _a;
                        var fieldProps = {
                            name: filter.id,
                            label: filter.name,
                            help: filter.description,
                            disabled: !hasAccess,
                        };
                        // Note by default, forms generate data in the format of:
                        // { [fieldName]: [value] }
                        // Endpoints for these filters expect data to be:
                        // { 'active': [value] }
                        return (<panels_1.PanelItem key={filter.id} noPadding>
                      <NestedForm apiMethod="PUT" apiEndpoint={"" + filtersEndpoint + filter.id + "/"} initialData={_a = {}, _a[filter.id] = filter.active, _a} saveOnBlur>
                        {filter.id !== 'legacy-browsers' ? (<fieldFromConfig_1.default key={filter.id} getData={function (data) { return ({ active: data[filter.id] }); }} field={tslib_1.__assign({ type: 'boolean' }, fieldProps)}/>) : (<formField_1.default inline={false} {...fieldProps} getData={function (data) { return ({ subfilters: tslib_1.__spreadArray([], tslib_1.__read(data[filter.id])) }); }}>
                            {function (_a) {
                                    var onChange = _a.onChange, onBlur = _a.onBlur;
                                    return (<LegacyBrowserFilterRow key={filter.id} data={filter} disabled={!hasAccess} onToggle={_this.handleLegacyChange.bind(_this, onChange, onBlur)}/>);
                                }}
                          </formField_1.default>)}
                      </NestedForm>
                    </panels_1.PanelItem>);
                    })}
              </panels_1.PanelBody>
            </panels_1.Panel>

            <form_1.default apiMethod="PUT" apiEndpoint={projectEndpoint} initialData={project.options} saveOnBlur onSubmitSuccess={_this.handleSubmit}>
              <jsonForm_1.default features={features} forms={inboundFilters_1.default} disabled={!hasAccess} renderFooter={_this.renderCustomFilters(!hasAccess)}/>
            </form_1.default>
          </React.Fragment>);
            }}
      </access_1.default>);
    };
    return ProjectFiltersSettings;
}(asyncComponent_1.default));
exports.default = ProjectFiltersSettings;
// TODO(ts): Understand why styled is not correctly inheriting props here
var NestedForm = styled_1.default(form_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var FilterGrid = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n"])));
var FilterGridItem = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  background: ", ";\n  border-radius: 3px;\n  flex: 1;\n  padding: 12px;\n  height: 100%;\n"], ["\n  display: flex;\n  align-items: center;\n  background: ", ";\n  border-radius: 3px;\n  flex: 1;\n  padding: 12px;\n  height: 100%;\n"])), function (p) { return p.theme.backgroundSecondary; });
// We want this wrapper to maining 30% width
var FilterGridItemWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  padding: 12px;\n  width: 50%;\n"], ["\n  padding: 12px;\n  width: 50%;\n"])));
var FilterItem = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n"])));
var FilterGridIcon = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  width: 38px;\n  height: 38px;\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: 38px 38px;\n  margin-right: 6px;\n  flex-shrink: 0;\n"], ["\n  width: 38px;\n  height: 38px;\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: 38px 38px;\n  margin-right: 6px;\n  flex-shrink: 0;\n"])));
var FilterTitle = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  font-size: 14px;\n  font-weight: bold;\n  line-height: 1;\n  white-space: nowrap;\n"], ["\n  font-size: 14px;\n  font-weight: bold;\n  line-height: 1;\n  white-space: nowrap;\n"])));
var FilterDescription = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: 12px;\n  line-height: 1;\n  white-space: nowrap;\n"], ["\n  color: ", ";\n  font-size: 12px;\n  line-height: 1;\n  white-space: nowrap;\n"])), function (p) { return p.theme.subText; });
var BulkFilter = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  padding: 0 12px;\n"], ["\n  text-align: right;\n  padding: 0 12px;\n"])));
var BulkFilterLabel = styled_1.default('span')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  margin-right: 6px;\n"], ["\n  font-weight: bold;\n  margin-right: 6px;\n"])));
var BulkFilterItem = styled_1.default('a')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  border-right: 1px solid #f1f2f3;\n  margin-right: 6px;\n  padding-right: 6px;\n\n  &:last-child {\n    border-right: none;\n    margin-right: 0;\n  }\n"], ["\n  border-right: 1px solid #f1f2f3;\n  margin-right: 6px;\n  padding-right: 6px;\n\n  &:last-child {\n    border-right: none;\n    margin-right: 0;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=projectFiltersSettings.jsx.map