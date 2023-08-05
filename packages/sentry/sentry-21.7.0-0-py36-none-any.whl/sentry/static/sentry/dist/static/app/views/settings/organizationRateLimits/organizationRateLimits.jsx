Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var rangeField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/rangeField"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var getRateLimitValues = function () {
    var steps = [];
    var i = 0;
    while (i <= 1000000) {
        steps.push(i);
        if (i < 10000) {
            i += 1000;
        }
        else if (i < 100000) {
            i += 10000;
        }
        else {
            i += 100000;
        }
    }
    return steps;
};
// We can just generate this once
var ACCOUNT_RATE_LIMIT_VALUES = getRateLimitValues();
var OrganizationRateLimit = function (_a) {
    // TODO(billy): Update organization.quota in organizationStore with new values
    var organization = _a.organization;
    var quota = organization.quota;
    var maxRate = quota.maxRate, maxRateInterval = quota.maxRateInterval, projectLimit = quota.projectLimit, accountLimit = quota.accountLimit;
    var initialData = {
        projectRateLimit: projectLimit || 100,
        accountRateLimit: accountLimit,
    };
    return (<div>
      <settingsPageHeader_1.default title={locale_1.t('Rate Limits')}/>

      <panels_1.Panel>
        <panels_1.PanelHeader>{locale_1.t('Adjust Limits')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <panels_1.PanelAlert type="info">
            {locale_1.t("Rate limits allow you to control how much data is stored for this\n                organization. When a rate is exceeded the system will begin discarding\n                data until the next interval.")}
          </panels_1.PanelAlert>

          <form_1.default data-test-id="rate-limit-editor" saveOnBlur allowUndo apiMethod="PUT" apiEndpoint={"/organizations/" + organization.slug + "/"} initialData={initialData}>
            {!maxRate ? (<rangeField_1.default name="accountRateLimit" label={locale_1.t('Account Limit')} min={0} max={1000000} allowedValues={ACCOUNT_RATE_LIMIT_VALUES} help={locale_1.t('The maximum number of events to accept across this entire organization.')} placeholder="e.g. 500" formatLabel={function (value) {
                return !value
                    ? locale_1.t('No Limit')
                    : locale_1.tct('[number] per hour', {
                        number: value.toLocaleString(),
                    });
            }}/>) : (<field_1.default label={locale_1.t('Account Limit')} help={locale_1.t('The maximum number of events to accept across this entire organization.')}>
                <textBlock_1.default css={{ marginBottom: 0 }}>
                  {locale_1.tct('Your account is limited to a maximum of [maxRate] events per [maxRateInterval] seconds.', {
                maxRate: maxRate,
                maxRateInterval: maxRateInterval,
            })}
                </textBlock_1.default>
              </field_1.default>)}
            <rangeField_1.default name="projectRateLimit" label={locale_1.t('Per-Project Limit')} help={locale_1.t('The maximum percentage of the account limit (set above) that an individual project can consume.')} step={5} min={50} max={100} formatLabel={function (value) {
            return value !== 100 ? (value + "%") : (<span dangerouslySetInnerHTML={{ __html: locale_1.t('No Limit') + " &mdash; 100%" }}/>);
        }}/>
          </form_1.default>
        </panels_1.PanelBody>
      </panels_1.Panel>
    </div>);
};
exports.default = OrganizationRateLimit;
//# sourceMappingURL=organizationRateLimits.jsx.map