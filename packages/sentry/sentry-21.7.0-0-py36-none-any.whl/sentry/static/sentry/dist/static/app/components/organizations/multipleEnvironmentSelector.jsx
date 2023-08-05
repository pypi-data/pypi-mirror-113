Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var uniq_1 = tslib_1.__importDefault(require("lodash/uniq"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var globalSelectionHeaderRow_1 = tslib_1.__importDefault(require("app/components/globalSelectionHeaderRow"));
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var headerItem_1 = tslib_1.__importDefault(require("app/components/organizations/headerItem"));
var multipleSelectorSubmitRow_1 = tslib_1.__importDefault(require("app/components/organizations/multipleSelectorSubmitRow"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var analytics_1 = require("app/utils/analytics");
var getRouteStringFromRoutes_1 = tslib_1.__importDefault(require("app/utils/getRouteStringFromRoutes"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
/**
 * Environment Selector
 *
 * Note we only fetch environments when this component is mounted
 */
var MultipleEnvironmentSelector = /** @class */ (function (_super) {
    tslib_1.__extends(MultipleEnvironmentSelector, _super);
    function MultipleEnvironmentSelector() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            selectedEnvs: new Set(_this.props.value),
            hasChanges: false,
        };
        _this.syncSelectedStateFromProps = function () {
            return _this.setState({ selectedEnvs: new Set(_this.props.value) });
        };
        /**
         * If value in state is different than value from props, propagate changes
         */
        _this.doChange = function (environments) {
            _this.props.onChange(environments);
        };
        /**
         * Checks if "onUpdate" is callable. Only calls if there are changes
         */
        _this.doUpdate = function () {
            _this.setState({ hasChanges: false }, _this.props.onUpdate);
        };
        /**
         * Toggle selected state of an environment
         */
        _this.toggleSelected = function (environment) {
            _this.setState(function (state) {
                var selectedEnvs = new Set(state.selectedEnvs);
                if (selectedEnvs.has(environment)) {
                    selectedEnvs.delete(environment);
                }
                else {
                    selectedEnvs.add(environment);
                }
                analytics_1.analytics('environmentselector.toggle', {
                    action: selectedEnvs.has(environment) ? 'added' : 'removed',
                    path: getRouteStringFromRoutes_1.default(_this.props.router.routes),
                    org_id: parseInt(_this.props.organization.id, 10),
                });
                _this.doChange(Array.from(selectedEnvs.values()));
                return {
                    selectedEnvs: selectedEnvs,
                    hasChanges: true,
                };
            });
        };
        /**
         * Calls "onUpdate" callback and closes the dropdown menu
         */
        _this.handleUpdate = function (actions) {
            actions.close();
            _this.doUpdate();
        };
        _this.handleClose = function () {
            // Only update if there are changes
            if (!_this.state.hasChanges) {
                return;
            }
            analytics_1.analytics('environmentselector.update', {
                count: _this.state.selectedEnvs.size,
                path: getRouteStringFromRoutes_1.default(_this.props.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            _this.doUpdate();
        };
        /**
         * Clears all selected environments and updates
         */
        _this.handleClear = function () {
            analytics_1.analytics('environmentselector.clear', {
                path: getRouteStringFromRoutes_1.default(_this.props.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState({
                hasChanges: false,
                selectedEnvs: new Set(),
            }, function () {
                _this.doChange([]);
                _this.doUpdate();
            });
        };
        /**
         * Selects an environment, should close menu and initiate an update
         */
        _this.handleSelect = function (item) {
            var environment = item.value;
            analytics_1.analytics('environmentselector.direct_selection', {
                path: getRouteStringFromRoutes_1.default(_this.props.router.routes),
                org_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState(function () {
                _this.doChange([environment]);
                return {
                    selectedEnvs: new Set([environment]),
                };
            }, _this.doUpdate);
        };
        /**
         * Handler for when an environment is selected by the multiple select component
         * Does not initiate an "update"
         */
        _this.handleMultiSelect = function (environment) {
            _this.toggleSelected(environment);
        };
        return _this;
    }
    MultipleEnvironmentSelector.prototype.componentDidUpdate = function (prevProps) {
        // Need to sync state
        if (this.props.value !== prevProps.value) {
            this.syncSelectedStateFromProps();
        }
    };
    MultipleEnvironmentSelector.prototype.getEnvironments = function () {
        var _a = this.props, projects = _a.projects, selectedProjects = _a.selectedProjects;
        var config = configStore_1.default.getConfig();
        var environments = [];
        projects.forEach(function (project) {
            var projectId = parseInt(project.id, 10);
            // Include environments from:
            // - all projects if the user is a superuser
            // - the requested projects
            // - all member projects if 'my projects' (empty list) is selected.
            // - all projects if -1 is the only selected project.
            if ((selectedProjects.length === 1 &&
                selectedProjects[0] === globalSelectionHeader_1.ALL_ACCESS_PROJECTS &&
                project.hasAccess) ||
                (selectedProjects.length === 0 &&
                    (project.isMember || config.user.isSuperuser)) ||
                selectedProjects.includes(projectId)) {
                environments = environments.concat(project.environments);
            }
        });
        return uniq_1.default(environments);
    };
    MultipleEnvironmentSelector.prototype.render = function () {
        var _this = this;
        var _a = this.props, value = _a.value, loadingProjects = _a.loadingProjects;
        var environments = this.getEnvironments();
        var validatedValue = value.filter(function (env) { return environments.includes(env); });
        var summary = validatedValue.length
            ? "" + validatedValue.join(', ')
            : locale_1.t('All Environments');
        return loadingProjects ? (<StyledHeaderItem data-test-id="global-header-environment-selector" icon={<icons_1.IconWindow />} loading={loadingProjects} hasChanges={false} hasSelected={false} isOpen={false} locked={false}>
        {locale_1.t('Loading\u2026')}
      </StyledHeaderItem>) : (<react_1.ClassNames>
        {function (_a) {
                var css = _a.css;
                return (<StyledDropdownAutoComplete alignMenu="left" allowActorToggle closeOnSelect blendCorner={false} searchPlaceholder={locale_1.t('Filter environments')} onSelect={_this.handleSelect} onClose={_this.handleClose} maxHeight={500} rootClassName={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n              position: relative;\n              display: flex;\n              left: -1px;\n            "], ["\n              position: relative;\n              display: flex;\n              left: -1px;\n            "])))} inputProps={{ style: { padding: 8, paddingLeft: 14 } }} emptyMessage={locale_1.t('You have no environments')} noResultsMessage={locale_1.t('No environments found')} virtualizedHeight={theme_1.default.headerSelectorRowHeight} emptyHidesInput menuFooter={function (_a) {
                        var actions = _a.actions;
                        return _this.state.hasChanges ? (<multipleSelectorSubmitRow_1.default onSubmit={function () { return _this.handleUpdate(actions); }}/>) : null;
                    }} items={environments.map(function (env) { return ({
                        value: env,
                        searchKey: env,
                        label: function (_a) {
                            var inputValue = _a.inputValue;
                            return (<EnvironmentSelectorItem environment={env} inputValue={inputValue} isChecked={_this.state.selectedEnvs.has(env)} onMultiSelect={_this.handleMultiSelect}/>);
                        },
                    }); })}>
            {function (_a) {
                        var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                        return (<StyledHeaderItem data-test-id="global-header-environment-selector" icon={<icons_1.IconWindow />} isOpen={isOpen} hasSelected={value && !!value.length} onClear={_this.handleClear} hasChanges={false} locked={false} loading={false} {...getActorProps()}>
                {summary}
              </StyledHeaderItem>);
                    }}
          </StyledDropdownAutoComplete>);
            }}
      </react_1.ClassNames>);
    };
    MultipleEnvironmentSelector.defaultProps = {
        value: [],
    };
    return MultipleEnvironmentSelector;
}(React.PureComponent));
exports.default = withApi_1.default(react_router_1.withRouter(MultipleEnvironmentSelector));
var StyledHeaderItem = styled_1.default(headerItem_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 100%;\n"], ["\n  height: 100%;\n"])));
var StyledDropdownAutoComplete = styled_1.default(dropdownAutoComplete_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: 100%;\n  box-shadow: ", ";\n  border-radius: ", ";\n  margin-top: 0;\n  min-width: 100%;\n"], ["\n  background: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: 100%;\n  box-shadow: ", ";\n  border-radius: ", ";\n  margin-top: 0;\n  min-width: 100%;\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.borderRadiusBottom; });
var EnvironmentSelectorItem = /** @class */ (function (_super) {
    tslib_1.__extends(EnvironmentSelectorItem, _super);
    function EnvironmentSelectorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleMultiSelect = function () {
            var _a = _this.props, environment = _a.environment, onMultiSelect = _a.onMultiSelect;
            onMultiSelect(environment);
        };
        _this.handleClick = function (e) {
            e.stopPropagation();
            _this.handleMultiSelect();
        };
        return _this;
    }
    EnvironmentSelectorItem.prototype.render = function () {
        var _a = this.props, environment = _a.environment, inputValue = _a.inputValue, isChecked = _a.isChecked;
        return (<globalSelectionHeaderRow_1.default data-test-id={"environment-" + environment} checked={isChecked} onCheckClick={this.handleClick}>
        <highlight_1.default text={inputValue}>{environment}</highlight_1.default>
      </globalSelectionHeaderRow_1.default>);
    };
    return EnvironmentSelectorItem;
}(React.PureComponent));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=multipleEnvironmentSelector.jsx.map