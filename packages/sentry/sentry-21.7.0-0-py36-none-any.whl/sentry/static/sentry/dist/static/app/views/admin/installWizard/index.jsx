Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_document_title_1 = tslib_1.__importDefault(require("react-document-title"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var sentry_pattern_png_1 = tslib_1.__importDefault(require("sentry-images/pattern/sentry-pattern.png"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var forms_1 = require("app/components/forms");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var options_1 = require("../options");
var InstallWizard = /** @class */ (function (_super) {
    tslib_1.__extends(InstallWizard, _super);
    function InstallWizard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InstallWizard.prototype.getEndpoints = function () {
        return [['data', '/internal/options/?query=is:required']];
    };
    InstallWizard.prototype.renderFormFields = function () {
        var e_1, _a;
        var options = this.state.data;
        var missingOptions = new Set(Object.keys(options).filter(function (option) { return !options[option].field.isSet; }));
        // This is to handle the initial installation case.
        // Even if all options are filled out, we want to prompt to confirm
        // them. This is a bit of a hack because we're assuming that
        // the backend only spit back all filled out options for
        // this case.
        if (missingOptions.size === 0) {
            missingOptions = new Set(Object.keys(options));
        }
        // A mapping of option name to Field object
        var fields = {};
        try {
            for (var missingOptions_1 = tslib_1.__values(missingOptions), missingOptions_1_1 = missingOptions_1.next(); !missingOptions_1_1.done; missingOptions_1_1 = missingOptions_1.next()) {
                var key = missingOptions_1_1.value;
                var option = options[key];
                if (option.field.disabled) {
                    continue;
                }
                fields[key] = options_1.getOptionField(key, option.field);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (missingOptions_1_1 && !missingOptions_1_1.done && (_a = missingOptions_1.return)) _a.call(missingOptions_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return options_1.getForm(fields);
    };
    InstallWizard.prototype.getInitialData = function () {
        var options = this.state.data;
        var data = {};
        Object.keys(options).forEach(function (optionName) {
            var option = options[optionName];
            if (option.field.disabled) {
                return;
            }
            // TODO(dcramer): we need to rethink this logic as doing multiple "is this value actually set"
            // is problematic
            // all values to their server-defaults (as client-side defaults dont really work)
            var displayValue = option.value || options_1.getOptionDefault(optionName);
            if (
            // XXX(dcramer): we need the user to explicitly choose beacon.anonymous
            // vs using an implied default so effectively this is binding
            optionName !== 'beacon.anonymous' &&
                // XXX(byk): if we don't have a set value but have a default value filled
                // instead, from the client, set it on the data so it is sent to the server
                !option.field.isSet &&
                displayValue !== undefined) {
                data[optionName] = displayValue;
            }
        });
        return data;
    };
    InstallWizard.prototype.getTitle = function () {
        return locale_1.t('Setup Sentry');
    };
    InstallWizard.prototype.render = function () {
        var version = configStore_1.default.get('version');
        return (<react_document_title_1.default title={this.getTitle()}>
        <Wrapper>
          <Pattern />
          <SetupWizard>
            <Heading>
              <span>{locale_1.t('Welcome to Sentry')}</span>
              <Version>{version.current}</Version>
            </Heading>
            {this.state.loading
                ? this.renderLoading()
                : this.state.error
                    ? this.renderError()
                    : this.renderBody()}
          </SetupWizard>
        </Wrapper>
      </react_document_title_1.default>);
    };
    InstallWizard.prototype.renderError = function () {
        return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
        {locale_1.t('We were unable to load the required configuration from the Sentry server. Please take a look at the service logs.')}
      </alert_1.default>);
    };
    InstallWizard.prototype.renderBody = function () {
        return (<forms_1.ApiForm apiMethod="PUT" apiEndpoint={this.getEndpoints()[0][1]} submitLabel={locale_1.t('Continue')} initialData={this.getInitialData()} onSubmitSuccess={this.props.onConfigured}>
        <p>{locale_1.t('Complete setup by filling out the required configuration.')}</p>

        {this.renderFormFields()}
      </forms_1.ApiForm>);
    };
    return InstallWizard;
}(asyncView_1.default));
exports.default = InstallWizard;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n"], ["\n  display: flex;\n  justify-content: center;\n"])));
var fixedStyle = react_1.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n"], ["\n  position: fixed;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  left: 0;\n"])));
var Pattern = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  &::before {\n    ", "\n    content: '';\n    background-image: linear-gradient(\n      to right,\n      ", " 0%,\n      ", " 100%\n    );\n    background-repeat: repeat-y;\n  }\n\n  &::after {\n    ", "\n    content: '';\n    background: url(", ");\n    background-size: 400px;\n    opacity: 0.8;\n  }\n"], ["\n  &::before {\n    ", "\n    content: '';\n    background-image: linear-gradient(\n      to right,\n      ", " 0%,\n      ", " 100%\n    );\n    background-repeat: repeat-y;\n  }\n\n  &::after {\n    ", "\n    content: '';\n    background: url(", ");\n    background-size: 400px;\n    opacity: 0.8;\n  }\n"])), fixedStyle, function (p) { return p.theme.purple200; }, function (p) { return p.theme.purple300; }, fixedStyle, sentry_pattern_png_1.default);
var Heading = styled_1.default('h1')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-content: space-between;\n  grid-auto-flow: column;\n  line-height: 36px;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-content: space-between;\n  grid-auto-flow: column;\n  line-height: 36px;\n"])), space_1.default(1));
var Version = styled_1.default('small')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  line-height: inherit;\n"], ["\n  font-size: ", ";\n  line-height: inherit;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var SetupWizard = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  background: ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  margin-top: 40px;\n  padding: 40px 40px 20px;\n  width: 600px;\n  z-index: ", ";\n"], ["\n  background: ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n  margin-top: 40px;\n  padding: 40px 40px 20px;\n  width: 600px;\n  z-index: ", ";\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowHeavy; }, function (p) { return p.theme.zIndex.initial; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map