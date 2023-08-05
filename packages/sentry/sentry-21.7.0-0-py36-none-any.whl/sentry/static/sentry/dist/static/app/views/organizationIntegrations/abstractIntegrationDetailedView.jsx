Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var startCase_1 = tslib_1.__importDefault(require("lodash/startCase"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panels_1 = require("app/components/panels");
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var pluginIcon_1 = tslib_1.__importDefault(require("app/plugins/components/pluginIcon"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var marked_1 = tslib_1.__importStar(require("app/utils/marked"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var RequestIntegrationButton_1 = tslib_1.__importDefault(require("./integrationRequest/RequestIntegrationButton"));
var integrationStatus_1 = tslib_1.__importDefault(require("./integrationStatus"));
var AbstractIntegrationDetailedView = /** @class */ (function (_super) {
    tslib_1.__extends(AbstractIntegrationDetailedView, _super);
    function AbstractIntegrationDetailedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.tabs = ['overview', 'configurations'];
        _this.onTabChange = function (value) {
            _this.trackIntegrationEvent('integrations.integration_tab_clicked', {
                integration_tab: value,
            });
            _this.setState({ tab: value });
        };
        // Wrapper around trackIntegrationEvent that automatically provides many fields and the org
        _this.trackIntegrationEvent = function (eventKey, options) {
            options = options || {};
            // If we use this intermediate type we get type checking on the things we care about
            var params = tslib_1.__assign({ view: 'integrations_directory_integration_detail', integration: _this.integrationSlug, integration_type: _this.integrationType, already_installed: _this.installationStatus !== 'Not Installed' }, options);
            integrationUtil_1.trackIntegrationEvent(eventKey, params, _this.props.organization);
        };
        return _this;
    }
    AbstractIntegrationDetailedView.prototype.componentDidMount = function () {
        var location = this.props.location;
        var value = location.query.tab === 'configurations' ? 'configurations' : 'overview';
        // eslint-disable-next-line react/no-did-mount-set-state
        this.setState({ tab: value });
    };
    AbstractIntegrationDetailedView.prototype.onLoadAllEndpointsSuccess = function () {
        this.trackIntegrationEvent('integrations.integration_viewed', {
            integration_tab: this.state.tab,
        });
    };
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "integrationType", {
        /**
         * Abstract methods defined below
         */
        // The analytics type used in analytics which is snake case
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "description", {
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "author", {
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "alerts", {
        get: function () {
            // default is no alerts
            return [];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "resourceLinks", {
        // Returns a list of the resources displayed at the bottom of the overview card
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "installationStatus", {
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "integrationName", {
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "featureData", {
        // Returns an array of RawIntegrationFeatures which is used in feature gating
        // and displaying what the integration does
        get: function () {
            // Allow children to implement this
            throw new Error('Not implemented');
        },
        enumerable: false,
        configurable: true
    });
    AbstractIntegrationDetailedView.prototype.getIcon = function (title) {
        switch (title) {
            case 'View Source':
                return <icons_1.IconProject />;
            case 'Report Issue':
                return <icons_1.IconGithub />;
            case 'Documentation':
            case 'Splunk Setup Instructions':
            case 'Trello Setup Instructions':
                return <icons_1.IconDocs />;
            default:
                return <icons_1.IconGeneric />;
        }
    };
    // Returns the string that is shown as the title of a tab
    AbstractIntegrationDetailedView.prototype.getTabDisplay = function (tab) {
        // default is return the tab
        return tab;
    };
    // Render the button at the top which is usually just an installation button
    AbstractIntegrationDetailedView.prototype.renderTopButton = function (_disabledFromFeatures, // from the feature gate
    _userHasAccess // from user permissions
    ) {
        // Allow children to implement this
        throw new Error('Not implemented');
    };
    // Returns the permission descriptions, only use by Sentry Apps
    AbstractIntegrationDetailedView.prototype.renderPermissions = function () {
        // default is don't render permissions
        return null;
    };
    AbstractIntegrationDetailedView.prototype.renderEmptyConfigurations = function () {
        return (<panels_1.Panel>
        <emptyMessage_1.default title={locale_1.t("You haven't set anything up yet")} description={locale_1.t('But that doesn’t have to be the case for long! Add an installation to get started.')} action={this.renderAddInstallButton(true)}/>
      </panels_1.Panel>);
    };
    // Returns the list of configurations for the integration
    AbstractIntegrationDetailedView.prototype.renderConfigurations = function () {
        // Allow children to implement this
        throw new Error('Not implemented');
    };
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "integrationSlug", {
        /**
         * Actually implemented methods below
         */
        get: function () {
            return this.props.params.integrationSlug;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AbstractIntegrationDetailedView.prototype, "featureProps", {
        // Returns the props as needed by the hooks integrations:feature-gates
        get: function () {
            var organization = this.props.organization;
            var featureData = this.featureData;
            // Prepare the features list
            var features = featureData.map(function (f) { return ({
                featureGate: f.featureGate,
                description: (<FeatureListItem dangerouslySetInnerHTML={{ __html: marked_1.singleLineRenderer(f.description) }}/>),
            }); });
            return { organization: organization, features: features };
        },
        enumerable: false,
        configurable: true
    });
    AbstractIntegrationDetailedView.prototype.cleanTags = function () {
        return integrationUtil_1.getCategories(this.featureData);
    };
    AbstractIntegrationDetailedView.prototype.renderRequestIntegrationButton = function () {
        return (<RequestIntegrationButton_1.default organization={this.props.organization} name={this.integrationName} slug={this.integrationSlug} type={this.integrationType}/>);
    };
    AbstractIntegrationDetailedView.prototype.renderAddInstallButton = function (hideButtonIfDisabled) {
        var _this = this;
        if (hideButtonIfDisabled === void 0) { hideButtonIfDisabled = false; }
        var organization = this.props.organization;
        var IntegrationDirectoryFeatures = integrationUtil_1.getIntegrationFeatureGate().IntegrationDirectoryFeatures;
        return (<IntegrationDirectoryFeatures {...this.featureProps}>
        {function (_a) {
                var disabled = _a.disabled, disabledReason = _a.disabledReason;
                return (<DisableWrapper>
            <access_1.default organization={organization} access={['org:integrations']}>
              {function (_a) {
                        var hasAccess = _a.hasAccess;
                        return (<tooltip_1.default title={locale_1.t('You must be an organization owner, manager or admin to install this.')} disabled={hasAccess}>
                  {!hideButtonIfDisabled && disabled ? (<div />) : (_this.renderTopButton(disabled, hasAccess))}
                </tooltip_1.default>);
                    }}
            </access_1.default>
            {disabled && <DisabledNotice reason={disabledReason}/>}
          </DisableWrapper>);
            }}
      </IntegrationDirectoryFeatures>);
    };
    // Returns the content shown in the top section of the integration detail
    AbstractIntegrationDetailedView.prototype.renderTopSection = function () {
        var tags = this.cleanTags();
        return (<Flex>
        <pluginIcon_1.default pluginId={this.integrationSlug} size={50}/>
        <NameContainer>
          <Flex>
            <Name>{this.integrationName}</Name>
            <StatusWrapper>
              {this.installationStatus && (<integrationStatus_1.default status={this.installationStatus}/>)}
            </StatusWrapper>
          </Flex>
          <Flex>
            {tags.map(function (feature) { return (<StyledTag key={feature}>{startCase_1.default(feature)}</StyledTag>); })}
          </Flex>
        </NameContainer>
        {this.renderAddInstallButton()}
      </Flex>);
    };
    // Returns the tabs divider with the clickable tabs
    AbstractIntegrationDetailedView.prototype.renderTabs = function () {
        var _this = this;
        // TODO: Convert to styled component
        return (<ul className="nav nav-tabs border-bottom" style={{ paddingTop: '30px' }}>
        {this.tabs.map(function (tabName) { return (<li key={tabName} className={_this.state.tab === tabName ? 'active' : ''} onClick={function () { return _this.onTabChange(tabName); }}>
            <CapitalizedLink>{locale_1.t(_this.getTabDisplay(tabName))}</CapitalizedLink>
          </li>); })}
      </ul>);
    };
    // Returns the information about the integration description and features
    AbstractIntegrationDetailedView.prototype.renderInformationCard = function () {
        var _this = this;
        var IntegrationDirectoryFeatureList = integrationUtil_1.getIntegrationFeatureGate().IntegrationDirectoryFeatureList;
        return (<React.Fragment>
        <Flex>
          <FlexContainer>
            <Description dangerouslySetInnerHTML={{ __html: marked_1.default(this.description) }}/>
            <IntegrationDirectoryFeatureList {...this.featureProps} provider={{ key: this.props.params.integrationSlug }}/>
            {this.renderPermissions()}
            {this.alerts.map(function (alert, i) { return (<alert_1.default key={i} type={alert.type} icon={alert.icon}>
                <span dangerouslySetInnerHTML={{ __html: marked_1.singleLineRenderer(alert.text) }}/>
              </alert_1.default>); })}
          </FlexContainer>
          <Metadata>
            {!!this.author && (<AuthorInfo>
                <CreatedContainer>{locale_1.t('Created By')}</CreatedContainer>
                <div>{this.author}</div>
              </AuthorInfo>)}
            {this.resourceLinks.map(function (_a) {
                var title = _a.title, url = _a.url;
                return (<ExternalLinkContainer key={url}>
                {_this.getIcon(title)}
                <externalLink_1.default href={url}>{locale_1.t(title)}</externalLink_1.default>
              </ExternalLinkContainer>);
            })}
          </Metadata>
        </Flex>
      </React.Fragment>);
    };
    AbstractIntegrationDetailedView.prototype.renderBody = function () {
        return (<React.Fragment>
        {this.renderTopSection()}
        {this.renderTabs()}
        {this.state.tab === 'overview'
                ? this.renderInformationCard()
                : this.renderConfigurations()}
      </React.Fragment>);
    };
    return AbstractIntegrationDetailedView;
}(asyncComponent_1.default));
var Flex = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var FlexContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var CapitalizedLink = styled_1.default('a')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  text-transform: capitalize;\n"], ["\n  text-transform: capitalize;\n"])));
var StyledTag = styled_1.default(tag_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  text-transform: none;\n  &:not(:first-child) {\n    margin-left: ", ";\n  }\n"], ["\n  text-transform: none;\n  &:not(:first-child) {\n    margin-left: ", ";\n  }\n"])), space_1.default(0.5));
var NameContainer = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  flex-direction: column;\n  justify-content: center;\n  padding-left: ", ";\n"], ["\n  display: flex;\n  align-items: flex-start;\n  flex-direction: column;\n  justify-content: center;\n  padding-left: ", ";\n"])), space_1.default(2));
var Name = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  font-size: 1.4em;\n  margin-bottom: ", ";\n"], ["\n  font-weight: bold;\n  font-size: 1.4em;\n  margin-bottom: ", ";\n"])), space_1.default(1));
var IconCloseCircle = styled_1.default(icons_1.IconClose)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-right: ", ";\n"], ["\n  color: ", ";\n  margin-right: ", ";\n"])), function (p) { return p.theme.red300; }, space_1.default(1));
var DisabledNotice = styled_1.default(function (_a) {
    var reason = _a.reason, p = tslib_1.__rest(_a, ["reason"]);
    return (<div style={{
            display: 'flex',
            alignItems: 'center',
        }} {...p}>
    <IconCloseCircle isCircled/>
    <span>{reason}</span>
  </div>);
})(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n  font-size: 0.9em;\n"], ["\n  padding-top: ", ";\n  font-size: 0.9em;\n"])), space_1.default(0.5));
var FeatureListItem = styled_1.default('span')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  line-height: 24px;\n"], ["\n  line-height: 24px;\n"])));
var Description = styled_1.default('div')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  font-size: 1.5rem;\n  line-height: 2.1rem;\n  margin-bottom: ", ";\n\n  li {\n    margin-bottom: 6px;\n  }\n"], ["\n  font-size: 1.5rem;\n  line-height: 2.1rem;\n  margin-bottom: ", ";\n\n  li {\n    margin-bottom: 6px;\n  }\n"])), space_1.default(2));
var Metadata = styled_1.default(Flex)(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-auto-rows: max-content;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n  font-size: 0.9em;\n  margin-left: ", ";\n  margin-right: 100px;\n"], ["\n  display: grid;\n  grid-auto-rows: max-content;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n  font-size: 0.9em;\n  margin-left: ", ";\n  margin-right: 100px;\n"])), space_1.default(2), space_1.default(4));
var AuthorInfo = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
var ExternalLinkContainer = styled_1.default('div')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(1));
var StatusWrapper = styled_1.default('div')(templateObject_14 || (templateObject_14 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  padding-left: ", ";\n  line-height: 1.5em;\n"], ["\n  margin-bottom: ", ";\n  padding-left: ", ";\n  line-height: 1.5em;\n"])), space_1.default(1), space_1.default(2));
var DisableWrapper = styled_1.default('div')(templateObject_15 || (templateObject_15 = tslib_1.__makeTemplateObject(["\n  margin-left: auto;\n  align-self: center;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"], ["\n  margin-left: auto;\n  align-self: center;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n"])));
var CreatedContainer = styled_1.default('div')(templateObject_16 || (templateObject_16 = tslib_1.__makeTemplateObject(["\n  text-transform: uppercase;\n  padding-bottom: ", ";\n  color: ", ";\n  font-weight: 600;\n  font-size: 12px;\n"], ["\n  text-transform: uppercase;\n  padding-bottom: ", ";\n  color: ", ";\n  font-weight: 600;\n  font-size: 12px;\n"])), space_1.default(1), function (p) { return p.theme.gray300; });
exports.default = AbstractIntegrationDetailedView;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=abstractIntegrationDetailedView.jsx.map