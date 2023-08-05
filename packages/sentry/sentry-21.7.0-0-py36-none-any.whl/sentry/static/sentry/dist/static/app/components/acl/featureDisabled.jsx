Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var selectText_1 = require("app/utils/selectText");
var installText = function (features, featureName) {
    return "# " + locale_1.t('Enables the %s feature', featureName) + "\n" + features
        .map(function (f) { return "SENTRY_FEATURES['" + f + "'] = True"; })
        .join('\n');
};
/**
 * DisabledInfo renders a component informing that a feature has been disabled.
 *
 * By default this component will render a help button which toggles more
 * information about why the feature is disabled, showing the missing feature
 * flag and linking to documentation for managing sentry server feature flags.
 */
var FeatureDisabled = /** @class */ (function (_super) {
    tslib_1.__extends(FeatureDisabled, _super);
    function FeatureDisabled() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showHelp: false,
        };
        _this.toggleHelp = function (e) {
            e.preventDefault();
            _this.setState(function (state) { return ({ showHelp: !state.showHelp }); });
        };
        return _this;
    }
    FeatureDisabled.prototype.renderFeatureDisabled = function () {
        var showHelp = this.state.showHelp;
        var _a = this.props, message = _a.message, features = _a.features, featureName = _a.featureName, hideHelpToggle = _a.hideHelpToggle;
        var showDescription = hideHelpToggle || showHelp;
        return (<React.Fragment>
        <FeatureDisabledMessage>
          {message}
          {!hideHelpToggle && (<HelpButton icon={showHelp ? (<icons_1.IconChevron direction="down" size="xs"/>) : (<icons_1.IconInfo size="xs"/>)} priority="link" size="xsmall" onClick={this.toggleHelp}>
              {locale_1.t('Help')}
            </HelpButton>)}
        </FeatureDisabledMessage>
        {showDescription && (<HelpDescription onClick={function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                }}>
            <p>
              {locale_1.tct("Enable this feature on your sentry installation by adding the\n              following configuration into your [configFile:sentry.conf.py].\n              See [configLink:the configuration documentation] for more\n              details.", {
                    configFile: <code />,
                    configLink: <externalLink_1.default href={constants_1.CONFIG_DOCS_URL}/>,
                })}
            </p>
            <clipboard_1.default hideUnsupported value={installText(features, featureName)}>
              <button_1.default borderless size="xsmall" onClick={function (e) {
                    e.stopPropagation();
                    e.preventDefault();
                }} icon={<icons_1.IconCopy size="xs"/>}>
                {locale_1.t('Copy to Clipboard')}
              </button_1.default>
            </clipboard_1.default>
            <pre onClick={function (e) { return selectText_1.selectText(e.target); }}>
              <code>{installText(features, featureName)}</code>
            </pre>
          </HelpDescription>)}
      </React.Fragment>);
    };
    FeatureDisabled.prototype.render = function () {
        var alert = this.props.alert;
        if (!alert) {
            return this.renderFeatureDisabled();
        }
        var AlertComponent = typeof alert === 'boolean' ? alert_1.default : alert;
        return (<AlertComponent type="warning" icon={<icons_1.IconLock size="xs"/>}>
        <AlertWrapper>{this.renderFeatureDisabled()}</AlertWrapper>
      </AlertComponent>);
    };
    FeatureDisabled.defaultProps = {
        message: locale_1.t('This feature is not enabled on your Sentry installation.'),
    };
    return FeatureDisabled;
}(React.Component));
var FeatureDisabledMessage = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var HelpButton = styled_1.default(button_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: 0.8em;\n"], ["\n  font-size: 0.8em;\n"])));
var HelpDescription = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: 0.9em;\n  margin-top: ", ";\n\n  p {\n    line-height: 1.5em;\n  }\n\n  pre,\n  code {\n    margin-bottom: 0;\n    white-space: pre;\n  }\n"], ["\n  font-size: 0.9em;\n  margin-top: ", ";\n\n  p {\n    line-height: 1.5em;\n  }\n\n  pre,\n  code {\n    margin-bottom: 0;\n    white-space: pre;\n  }\n"])), space_1.default(1));
var AlertWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", " {\n    color: #6d6319;\n    &:hover {\n      color: #88750b;\n    }\n  }\n\n  pre,\n  code {\n    background: #fbf7e0;\n  }\n"], ["\n  ", " {\n    color: #6d6319;\n    &:hover {\n      color: #88750b;\n    }\n  }\n\n  pre,\n  code {\n    background: #fbf7e0;\n  }\n"])), HelpButton);
exports.default = FeatureDisabled;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=featureDisabled.jsx.map