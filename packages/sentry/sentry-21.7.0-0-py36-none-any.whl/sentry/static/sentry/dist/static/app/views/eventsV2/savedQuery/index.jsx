Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var banner_1 = tslib_1.__importDefault(require("app/components/banner"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var createAlertButton_1 = require("app/components/createAlertButton");
var dropdownControl_1 = tslib_1.__importDefault(require("app/components/dropdownControl"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var eventView_1 = tslib_1.__importDefault(require("app/utils/discover/eventView"));
var urls_1 = require("app/utils/discover/urls");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var utils_1 = require("./utils");
var SavedQueryButtonGroup = /** @class */ (function (_super) {
    tslib_1.__extends(SavedQueryButtonGroup, _super);
    function SavedQueryButtonGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isNewQuery: true,
            isEditingQuery: false,
            queryName: '',
        };
        _this.onBlurInput = function (event) {
            var target = event.target;
            _this.setState({ queryName: target.value });
        };
        _this.onChangeInput = function (event) {
            var target = event.target;
            _this.setState({ queryName: target.value });
        };
        /**
         * There are two ways to create a query
         * 1) Creating a query from scratch and saving it
         * 2) Modifying an existing query and saving it
         */
        _this.handleCreateQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView;
            if (!_this.state.queryName) {
                return;
            }
            var nextEventView = eventView.clone();
            nextEventView.name = _this.state.queryName;
            // Checks if "Save as" button is clicked from a clean state, or it is
            // clicked while modifying an existing query
            var isNewQuery = !eventView.id;
            utils_1.handleCreateQuery(api, organization, nextEventView, isNewQuery).then(function (savedQuery) {
                var view = eventView_1.default.fromSavedQuery(savedQuery);
                banner_1.default.dismiss('discover');
                _this.setState({ queryName: '' });
                react_router_1.browserHistory.push(view.getResultsViewUrlTarget(organization.slug));
            });
        };
        _this.handleUpdateQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView, updateCallback = _a.updateCallback;
            utils_1.handleUpdateQuery(api, organization, eventView).then(function (savedQuery) {
                var view = eventView_1.default.fromSavedQuery(savedQuery);
                _this.setState({ queryName: '' });
                react_router_1.browserHistory.push(view.getResultsViewShortUrlTarget(organization.slug));
                updateCallback();
            });
        };
        _this.handleDeleteQuery = function (event) {
            event.preventDefault();
            event.stopPropagation();
            var _a = _this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView;
            utils_1.handleDeleteQuery(api, organization, eventView).then(function () {
                react_router_1.browserHistory.push({
                    pathname: urls_1.getDiscoverLandingUrl(organization),
                    query: {},
                });
            });
        };
        _this.handleCreateAlertSuccess = function () {
            var organization = _this.props.organization;
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.create_alert_clicked',
                eventName: 'Discoverv2: Create alert clicked',
                status: 'success',
                organization_id: organization.id,
                url: window.location.href,
            });
        };
        return _this;
    }
    SavedQueryButtonGroup.getDerivedStateFromProps = function (nextProps, prevState) {
        var nextEventView = nextProps.eventView, savedQuery = nextProps.savedQuery, savedQueryLoading = nextProps.savedQueryLoading;
        // For a new unsaved query
        if (!savedQuery) {
            return {
                isNewQuery: true,
                isEditingQuery: false,
                queryName: prevState.queryName || '',
            };
        }
        if (savedQueryLoading) {
            return prevState;
        }
        var savedEventView = eventView_1.default.fromSavedQuery(savedQuery);
        // Switching from a SavedQuery to another SavedQuery
        if (savedEventView.id !== nextEventView.id) {
            return {
                isNewQuery: false,
                isEditingQuery: false,
                queryName: '',
            };
        }
        // For modifying a SavedQuery
        var isEqualQuery = nextEventView.isEqualTo(savedEventView);
        return {
            isNewQuery: false,
            isEditingQuery: !isEqualQuery,
            // HACK(leedongwei): See comment at SavedQueryButtonGroup.onFocusInput
            queryName: prevState.queryName || '',
        };
    };
    SavedQueryButtonGroup.prototype.renderButtonSaveAs = function (disabled) {
        var queryName = this.state.queryName;
        /**
         * For a great UX, we should focus on `ButtonSaveInput` when `ButtonSave`
         * is clicked. However, `DropdownControl` wraps them in a FunctionComponent
         * which breaks `React.createRef`.
         */
        return (<dropdownControl_1.default alignRight menuWidth="220px" priority="default" buttonProps={{
                'aria-label': locale_1.t('Save as'),
                showChevron: false,
                icon: <icons_1.IconStar />,
                disabled: disabled,
            }} label={locale_1.t('Save as') + "\u2026"}>
        <ButtonSaveDropDown onClick={SavedQueryButtonGroup.stopEventPropagation}>
          <ButtonSaveInput type="text" name="query_name" placeholder={locale_1.t('Display name')} value={queryName || ''} onBlur={this.onBlurInput} onChange={this.onChangeInput} disabled={disabled}/>
          <button_1.default onClick={this.handleCreateQuery} priority="primary" disabled={disabled || !this.state.queryName} style={{ width: '100%' }}>
            {locale_1.t('Save for Org')}
          </button_1.default>
        </ButtonSaveDropDown>
      </dropdownControl_1.default>);
    };
    SavedQueryButtonGroup.prototype.renderButtonSave = function (disabled) {
        var _a = this.state, isNewQuery = _a.isNewQuery, isEditingQuery = _a.isEditingQuery;
        // Existing query that hasn't been modified.
        if (!isNewQuery && !isEditingQuery) {
            return (<button_1.default icon={<icons_1.IconStar color="yellow100" isSolid size="sm"/>} disabled data-test-id="discover2-savedquery-button-saved">
          {locale_1.t('Saved for Org')}
        </button_1.default>);
        }
        // Existing query with edits, show save and save as.
        if (!isNewQuery && isEditingQuery) {
            return (<React.Fragment>
          <button_1.default onClick={this.handleUpdateQuery} data-test-id="discover2-savedquery-button-update" disabled={disabled}>
            <IconUpdate />
            {locale_1.t('Save Changes')}
          </button_1.default>
          {this.renderButtonSaveAs(disabled)}
        </React.Fragment>);
        }
        // Is a new query enable saveas
        return this.renderButtonSaveAs(disabled);
    };
    SavedQueryButtonGroup.prototype.renderButtonDelete = function (disabled) {
        var isNewQuery = this.state.isNewQuery;
        if (isNewQuery) {
            return null;
        }
        return (<button_1.default data-test-id="discover2-savedquery-button-delete" onClick={this.handleDeleteQuery} disabled={disabled} icon={<icons_1.IconDelete />}/>);
    };
    SavedQueryButtonGroup.prototype.renderButtonCreateAlert = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, onIncompatibleAlertQuery = _a.onIncompatibleAlertQuery;
        return (<guideAnchor_1.default target="create_alert_from_discover">
        <createAlertButton_1.CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={onIncompatibleAlertQuery} onSuccess={this.handleCreateAlertSuccess} referrer="discover" data-test-id="discover2-create-from-discover"/>
      </guideAnchor_1.default>);
    };
    SavedQueryButtonGroup.prototype.render = function () {
        var _this = this;
        var organization = this.props.organization;
        var renderDisabled = function (p) { return (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={locale_1.t('Discover queries are disabled')} featureName={locale_1.t('Discover queries')}/>}>
        {p.children(p)}
      </hovercard_1.default>); };
        var renderQueryButton = function (renderFunc) {
            return (<feature_1.default organization={organization} features={['discover-query']} hookName="feature-disabled:discover-saved-query-create" renderDisabled={renderDisabled}>
          {function (_a) {
                var hasFeature = _a.hasFeature;
                return renderFunc(!hasFeature || _this.props.disabled);
            }}
        </feature_1.default>);
        };
        return (<ResponsiveButtonBar gap={1}>
        {renderQueryButton(function (disabled) { return _this.renderButtonSave(disabled); })}
        <feature_1.default organization={organization} features={['incidents']}>
          {function (_a) {
            var hasFeature = _a.hasFeature;
            return hasFeature && _this.renderButtonCreateAlert();
        }}
        </feature_1.default>
        {renderQueryButton(function (disabled) { return _this.renderButtonDelete(disabled); })}
      </ResponsiveButtonBar>);
    };
    /**
     * Stop propagation for the input and container so people can interact with
     * the inputs in the dropdown.
     */
    SavedQueryButtonGroup.stopEventPropagation = function (event) {
        var capturedElements = ['LI', 'INPUT'];
        if (event.target instanceof Element &&
            capturedElements.includes(event.target.nodeName)) {
            event.preventDefault();
            event.stopPropagation();
        }
    };
    SavedQueryButtonGroup.defaultProps = {
        disabled: false,
    };
    return SavedQueryButtonGroup;
}(React.PureComponent));
var ResponsiveButtonBar = styled_1.default(buttonBar_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-top: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var ButtonSaveDropDown = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  padding: ", ";\n  gap: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  padding: ", ";\n  gap: ", ";\n"])), space_1.default(1), space_1.default(1));
var ButtonSaveInput = styled_1.default(input_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  height: 40px;\n"], ["\n  height: 40px;\n"])));
var IconUpdate = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  width: 10px;\n  height: 10px;\n\n  margin-right: ", ";\n  border-radius: 5px;\n  background-color: ", ";\n"], ["\n  display: inline-block;\n  width: 10px;\n  height: 10px;\n\n  margin-right: ", ";\n  border-radius: 5px;\n  background-color: ", ";\n"])), space_1.default(0.75), function (p) { return p.theme.yellow300; });
exports.default = withProjects_1.default(withApi_1.default(SavedQueryButtonGroup));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map