Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var rangeSlider_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/rangeSlider"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var RATE_LIMIT_FORMAT_MAP = new Map([
    [0, 'None'],
    [60, '1 minute'],
    [300, '5 minutes'],
    [900, '15 minutes'],
    [3600, '1 hour'],
    [7200, '2 hours'],
    [14400, '4 hours'],
    [21600, '6 hours'],
    [43200, '12 hours'],
    [86400, '24 hours'],
]);
// This value isn't actually any, but the various angles on the types don't line up.
var formatRateLimitWindow = function (val) { return RATE_LIMIT_FORMAT_MAP.get(val); };
var KeyRateLimitsForm = /** @class */ (function (_super) {
    tslib_1.__extends(KeyRateLimitsForm, _super);
    function KeyRateLimitsForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeWindow = function (onChange, onBlur, currentValueObj, value, e) {
            var valueObj = tslib_1.__assign(tslib_1.__assign({}, currentValueObj), { window: value });
            onChange(valueObj, e);
            onBlur(valueObj, e);
        };
        _this.handleChangeCount = function (cb, value, e) {
            var valueObj = tslib_1.__assign(tslib_1.__assign({}, value), { count: e.target.value });
            cb(valueObj, e);
        };
        return _this;
    }
    KeyRateLimitsForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, data = _a.data, disabled = _a.disabled;
        var _b = this.props.params, keyId = _b.keyId, orgId = _b.orgId, projectId = _b.projectId;
        var apiEndpoint = "/projects/" + orgId + "/" + projectId + "/keys/" + keyId + "/";
        var disabledAlert = function (_a) {
            var features = _a.features;
            return (<featureDisabled_1.default alert={panels_1.PanelAlert} features={features} featureName={locale_1.t('Key Rate Limits')}/>);
        };
        return (<form_1.default saveOnBlur apiEndpoint={apiEndpoint} apiMethod="PUT" initialData={data}>
        <feature_1.default features={['projects:rate-limits']} hookName="feature-disabled:rate-limits" renderDisabled={function (_a) {
                var children = _a.children, props = tslib_1.__rest(_a, ["children"]);
                return typeof children === 'function' &&
                    children(tslib_1.__assign(tslib_1.__assign({}, props), { renderDisabled: disabledAlert }));
            }}>
          {function (_a) {
                var hasFeature = _a.hasFeature, features = _a.features, organization = _a.organization, project = _a.project, renderDisabled = _a.renderDisabled;
                return (<panels_1.Panel>
              <panels_1.PanelHeader>{locale_1.t('Rate Limits')}</panels_1.PanelHeader>

              <panels_1.PanelBody>
                <panels_1.PanelAlert type="info" icon={<icons_1.IconFlag size="md"/>}>
                  {locale_1.t("Rate limits provide a flexible way to manage your error\n                      volume. If you have a noisy project or environment you\n                      can configure a rate limit for this key to reduce the\n                      number of errors processed. To manage your transaction\n                      volume, we recommend adjusting your sample rate in your\n                      SDK configuration.")}
                </panels_1.PanelAlert>
                {!hasFeature &&
                        typeof renderDisabled === 'function' &&
                        renderDisabled({
                            organization: organization,
                            project: project,
                            features: features,
                            hasFeature: hasFeature,
                            children: null,
                        })}
                <formField_1.default className="rate-limit-group" name="rateLimit" label={locale_1.t('Rate Limit')} disabled={disabled || !hasFeature} validate={function (_a) {
                        var form = _a.form;
                        // TODO(TS): is validate actually doing anything because it's an unexpected prop
                        var isValid = form &&
                            form.rateLimit &&
                            typeof form.rateLimit.count !== 'undefined' &&
                            typeof form.rateLimit.window !== 'undefined';
                        if (isValid) {
                            return [];
                        }
                        return [['rateLimit', locale_1.t('Fill in both fields first')]];
                    }} formatMessageValue={function (value) {
                        return locale_1.t('%s errors in %s', value.count, formatRateLimitWindow(value.window));
                    }} help={locale_1.t('Apply a rate limit to this credential to cap the amount of errors accepted during a time window.')} inline={false}>
                  {function (_a) {
                        var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value;
                        return (<RateLimitRow>
                      <input_1.default type="number" name="rateLimit.count" min={0} value={value && value.count} placeholder={locale_1.t('Count')} disabled={disabled || !hasFeature} onChange={_this.handleChangeCount.bind(_this, onChange, value)} onBlur={_this.handleChangeCount.bind(_this, onBlur, value)}/>
                      <EventsIn>{locale_1.t('event(s) in')}</EventsIn>
                      <rangeSlider_1.default name="rateLimit.window" allowedValues={Array.from(RATE_LIMIT_FORMAT_MAP.keys())} value={value && value.window} placeholder={locale_1.t('Window')} formatLabel={formatRateLimitWindow} disabled={disabled || !hasFeature} onChange={_this.handleChangeWindow.bind(_this, onChange, onBlur, value)}/>
                    </RateLimitRow>);
                    }}
                </formField_1.default>
              </panels_1.PanelBody>
            </panels_1.Panel>);
            }}
        </feature_1.default>
      </form_1.default>);
    };
    return KeyRateLimitsForm;
}(React.Component));
exports.default = KeyRateLimitsForm;
var RateLimitRow = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 2fr 1fr 2fr;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 2fr 1fr 2fr;\n  align-items: center;\n  grid-gap: ", ";\n"])), space_1.default(1));
var EventsIn = styled_1.default('small')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  text-align: center;\n  white-space: nowrap;\n"], ["\n  font-size: ", ";\n  text-align: center;\n  white-space: nowrap;\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=keyRateLimitsForm.jsx.map