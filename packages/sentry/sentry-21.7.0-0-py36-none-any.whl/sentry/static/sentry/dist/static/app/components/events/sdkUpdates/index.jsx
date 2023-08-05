Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getSdkUpdateSuggestion_1 = tslib_1.__importDefault(require("app/utils/getSdkUpdateSuggestion"));
var SdkUpdates = function (_a) {
    var event = _a.event;
    var sdkUpdates = event.sdkUpdates;
    var eventDataSectinContent = sdkUpdates
        .map(function (sdkUpdate, index) {
        var suggestion = getSdkUpdateSuggestion_1.default({ suggestion: sdkUpdate, sdk: event.sdk });
        if (!suggestion) {
            return null;
        }
        return (<alert_1.default key={index} type="info" icon={<icons_1.IconUpgrade />}>
          {locale_1.tct('We recommend you [suggestion] ', { suggestion: suggestion })}
          {sdkUpdate.type === 'updateSdk' &&
                locale_1.t('(All sentry packages should be updated and their versions should match)')}
        </alert_1.default>);
    })
        .filter(function (alert) { return !!alert; });
    if (!eventDataSectinContent.length) {
        return null;
    }
    return (<eventDataSection_1.default title={null} type="sdk-updates">
      {eventDataSectinContent}
    </eventDataSection_1.default>);
};
exports.default = SdkUpdates;
//# sourceMappingURL=index.jsx.map