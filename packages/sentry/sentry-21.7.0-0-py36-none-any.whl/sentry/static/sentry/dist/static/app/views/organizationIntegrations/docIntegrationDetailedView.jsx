Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var abstractIntegrationDetailedView_1 = tslib_1.__importDefault(require("./abstractIntegrationDetailedView"));
var constants_1 = require("./constants");
var SentryAppDetailedView = /** @class */ (function (_super) {
    tslib_1.__extends(SentryAppDetailedView, _super);
    function SentryAppDetailedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.tabs = ['overview'];
        _this.trackClick = function () {
            _this.trackIntegrationEvent('integrations.installation_start');
        };
        return _this;
    }
    Object.defineProperty(SentryAppDetailedView.prototype, "integrationType", {
        get: function () {
            return 'document';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "integration", {
        get: function () {
            var integrationSlug = this.props.params.integrationSlug;
            var documentIntegration = constants_1.documentIntegrations[integrationSlug];
            if (!documentIntegration) {
                throw new Error("No document integration of slug " + integrationSlug + " exists");
            }
            return documentIntegration;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "description", {
        get: function () {
            return this.integration.description;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "author", {
        get: function () {
            return this.integration.author;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "resourceLinks", {
        get: function () {
            return this.integration.resourceLinks;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "installationStatus", {
        get: function () {
            return null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "integrationName", {
        get: function () {
            return this.integration.name;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryAppDetailedView.prototype, "featureData", {
        get: function () {
            return this.integration.features;
        },
        enumerable: false,
        configurable: true
    });
    SentryAppDetailedView.prototype.componentDidMount = function () {
        _super.prototype.componentDidMount.call(this);
        this.trackIntegrationEvent('integrations.integration_viewed', {
            integration_tab: 'overview',
        });
    };
    SentryAppDetailedView.prototype.renderTopButton = function () {
        return (<externalLink_1.default href={this.integration.docUrl} onClick={this.trackClick}>
        <LearnMoreButton size="small" priority="primary" style={{ marginLeft: space_1.default(1) }} data-test-id="learn-more" icon={<StyledIconOpen size="xs"/>}>
          {locale_1.t('Learn More')}
        </LearnMoreButton>
      </externalLink_1.default>);
    };
    // No configurations.
    SentryAppDetailedView.prototype.renderConfigurations = function () {
        return null;
    };
    return SentryAppDetailedView;
}(abstractIntegrationDetailedView_1.default));
var LearnMoreButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
var StyledIconOpen = styled_1.default(icons_1.IconOpen)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  transition: 0.1s linear color;\n  margin: 0 ", ";\n  position: relative;\n  top: 1px;\n"], ["\n  transition: 0.1s linear color;\n  margin: 0 ", ";\n  position: relative;\n  top: 1px;\n"])), space_1.default(0.5));
exports.default = withOrganization_1.default(SentryAppDetailedView);
var templateObject_1, templateObject_2;
//# sourceMappingURL=docIntegrationDetailedView.jsx.map