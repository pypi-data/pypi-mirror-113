Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var circleIndicator_1 = tslib_1.__importDefault(require("app/components/circleIndicator"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var pluginIcon_1 = tslib_1.__importDefault(require("app/plugins/components/pluginIcon"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var consolidatedScopes_1 = require("app/utils/consolidatedScopes");
var integrationUtil_1 = require("app/utils/integrationUtil");
var marked_1 = tslib_1.__importStar(require("app/utils/marked"));
var recordSentryAppInteraction_1 = require("app/utils/recordSentryAppInteraction");
// No longer a modal anymore but yea :)
var SentryAppDetailsModal = /** @class */ (function (_super) {
    tslib_1.__extends(SentryAppDetailsModal, _super);
    function SentryAppDetailsModal() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SentryAppDetailsModal.prototype.componentDidUpdate = function (prevProps) {
        // if the user changes org, count this as a fresh event to track
        if (this.props.organization.id !== prevProps.organization.id) {
            this.trackOpened();
        }
    };
    SentryAppDetailsModal.prototype.componentDidMount = function () {
        this.trackOpened();
    };
    SentryAppDetailsModal.prototype.trackOpened = function () {
        var _a = this.props, sentryApp = _a.sentryApp, organization = _a.organization, isInstalled = _a.isInstalled;
        recordSentryAppInteraction_1.recordInteraction(sentryApp.slug, 'sentry_app_viewed');
        integrationUtil_1.trackIntegrationEvent('integrations.install_modal_opened', {
            integration_type: 'sentry_app',
            integration: sentryApp.slug,
            already_installed: isInstalled,
            view: 'external_install',
            integration_status: sentryApp.status,
        }, organization, { startSession: true });
    };
    SentryAppDetailsModal.prototype.getEndpoints = function () {
        var sentryApp = this.props.sentryApp;
        return [['featureData', "/sentry-apps/" + sentryApp.slug + "/features/"]];
    };
    SentryAppDetailsModal.prototype.featureTags = function (features) {
        return features.map(function (feature) {
            var feat = feature.featureGate.replace(/integrations/g, '');
            return <StyledTag key={feat}>{feat.replace(/-/g, ' ')}</StyledTag>;
        });
    };
    Object.defineProperty(SentryAppDetailsModal.prototype, "permissions", {
        get: function () {
            return consolidatedScopes_1.toPermissions(this.props.sentryApp.scopes);
        },
        enumerable: false,
        configurable: true
    });
    SentryAppDetailsModal.prototype.onInstall = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var onInstall, _err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        onInstall = this.props.onInstall;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, onInstall()];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    SentryAppDetailsModal.prototype.renderPermissions = function () {
        var permissions = this.permissions;
        if (Object.keys(permissions).filter(function (scope) { return permissions[scope].length > 0; }).length === 0) {
            return null;
        }
        return (<React.Fragment>
        <Title>Permissions</Title>
        {permissions.read.length > 0 && (<Permission>
            <Indicator />
            <Text key="read">
              {locale_1.tct('[read] access to [resources] resources', {
                    read: <strong>Read</strong>,
                    resources: permissions.read.join(', '),
                })}
            </Text>
          </Permission>)}
        {permissions.write.length > 0 && (<Permission>
            <Indicator />
            <Text key="write">
              {locale_1.tct('[read] and [write] access to [resources] resources', {
                    read: <strong>Read</strong>,
                    write: <strong>Write</strong>,
                    resources: permissions.write.join(', '),
                })}
            </Text>
          </Permission>)}
        {permissions.admin.length > 0 && (<Permission>
            <Indicator />
            <Text key="admin">
              {locale_1.tct('[admin] access to [resources] resources', {
                    admin: <strong>Admin</strong>,
                    resources: permissions.admin.join(', '),
                })}
            </Text>
          </Permission>)}
      </React.Fragment>);
    };
    SentryAppDetailsModal.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, sentryApp = _a.sentryApp, closeModal = _a.closeModal, isInstalled = _a.isInstalled, organization = _a.organization;
        var featureData = this.state.featureData;
        // Prepare the features list
        var features = (featureData || []).map(function (f) { return ({
            featureGate: f.featureGate,
            description: (<span dangerouslySetInnerHTML={{ __html: marked_1.singleLineRenderer(f.description) }}/>),
        }); });
        var _b = integrationUtil_1.getIntegrationFeatureGate(), FeatureList = _b.FeatureList, IntegrationFeatures = _b.IntegrationFeatures;
        var overview = sentryApp.overview || '';
        var featureProps = { organization: organization, features: features };
        return (<React.Fragment>
        <Heading>
          <pluginIcon_1.default pluginId={sentryApp.slug} size={50}/>

          <HeadingInfo>
            <Name>{sentryApp.name}</Name>
            {!!features.length && <Features>{this.featureTags(features)}</Features>}
          </HeadingInfo>
        </Heading>

        <Description dangerouslySetInnerHTML={{ __html: marked_1.default(overview) }}/>
        <FeatureList {...featureProps} provider={tslib_1.__assign(tslib_1.__assign({}, sentryApp), { key: sentryApp.slug })}/>

        <IntegrationFeatures {...featureProps}>
          {function (_a) {
                var disabled = _a.disabled, disabledReason = _a.disabledReason;
                return (<React.Fragment>
              {!disabled && _this.renderPermissions()}
              <Footer>
                <Author>{locale_1.t('Authored By %s', sentryApp.author)}</Author>
                <div>
                  {disabled && <DisabledNotice reason={disabledReason}/>}
                  <button_1.default size="small" onClick={closeModal}>
                    {locale_1.t('Cancel')}
                  </button_1.default>

                  <access_1.default organization={organization} access={['org:integrations']}>
                    {function (_a) {
                        var hasAccess = _a.hasAccess;
                        return hasAccess && (<button_1.default size="small" priority="primary" disabled={isInstalled || disabled} onClick={function () { return _this.onInstall(); }} style={{ marginLeft: space_1.default(1) }} data-test-id="install">
                          {locale_1.t('Accept & Install')}
                        </button_1.default>);
                    }}
                  </access_1.default>
                </div>
              </Footer>
            </React.Fragment>);
            }}
        </IntegrationFeatures>
      </React.Fragment>);
    };
    return SentryAppDetailsModal;
}(asyncComponent_1.default));
exports.default = SentryAppDetailsModal;
var Heading = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-bottom: ", ";\n"])), space_1.default(1), space_1.default(2));
var HeadingInfo = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-rows: max-content max-content;\n  align-items: start;\n"], ["\n  display: grid;\n  grid-template-rows: max-content max-content;\n  align-items: start;\n"])));
var Name = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n  font-size: 1.4em;\n"], ["\n  font-weight: bold;\n  font-size: 1.4em;\n"])));
var Description = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-size: 1.5rem;\n  line-height: 2.1rem;\n  margin-bottom: ", ";\n\n  li {\n    margin-bottom: 6px;\n  }\n"], ["\n  font-size: 1.5rem;\n  line-height: 2.1rem;\n  margin-bottom: ", ";\n\n  li {\n    margin-bottom: 6px;\n  }\n"])), space_1.default(2));
var Author = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var DisabledNotice = styled_1.default(function (_a) {
    var reason = _a.reason, p = tslib_1.__rest(_a, ["reason"]);
    return (<div {...p}>
    <icons_1.IconFlag color="red300" size="1.5em"/>
    {reason}
  </div>);
})(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  flex: 1;\n  grid-template-columns: max-content 1fr;\n  color: ", ";\n  font-size: 0.9em;\n"], ["\n  display: grid;\n  align-items: center;\n  flex: 1;\n  grid-template-columns: max-content 1fr;\n  color: ", ";\n  font-size: 0.9em;\n"])), function (p) { return p.theme.red300; });
var Text = styled_1.default('p')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin: 0px 6px;\n"], ["\n  margin: 0px 6px;\n"])));
var Permission = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var Footer = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  padding: 20px 30px;\n  border-top: 1px solid #e2dee6;\n  margin: 20px -30px -30px;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  padding: 20px 30px;\n  border-top: 1px solid #e2dee6;\n  margin: 20px -30px -30px;\n  justify-content: space-between;\n"])));
var Title = styled_1.default('p')(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  font-weight: bold;\n"], ["\n  margin-bottom: ", ";\n  font-weight: bold;\n"])), space_1.default(1));
var Indicator = styled_1.default(function (p) { return <circleIndicator_1.default size={7} {...p}/>; })(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  margin-top: 7px;\n  color: ", ";\n"], ["\n  margin-top: 7px;\n  color: ", ";\n"])), function (p) { return p.theme.success; });
var Features = styled_1.default('div')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  margin: -", ";\n"], ["\n  margin: -", ";\n"])), space_1.default(0.5));
var StyledTag = styled_1.default(tag_1.default)(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space_1.default(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=sentryAppDetailsModal.jsx.map