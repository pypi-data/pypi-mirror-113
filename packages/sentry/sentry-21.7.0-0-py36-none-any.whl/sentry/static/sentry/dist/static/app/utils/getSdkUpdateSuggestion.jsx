Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function getSdkUpdateSuggestion(_a) {
    var sdk = _a.sdk, suggestion = _a.suggestion, _b = _a.shortStyle, shortStyle = _b === void 0 ? false : _b, _c = _a.capitalized, capitalized = _c === void 0 ? false : _c;
    function getUpdateSdkContent(newSdkVersion) {
        var _a, _b, _c, _d;
        if (capitalized) {
            return sdk
                ? shortStyle
                    ? locale_1.tct('Update to @v[new-sdk-version]', (_a = {},
                        _a['new-sdk-version'] = newSdkVersion,
                        _a))
                    : locale_1.tct('Update your SDK from @v[sdk-version] to @v[new-sdk-version]', (_b = {},
                        _b['sdk-version'] = sdk.version,
                        _b['new-sdk-version'] = newSdkVersion,
                        _b))
                : locale_1.t('Update your SDK version');
        }
        return sdk
            ? shortStyle
                ? locale_1.tct('update to @v[new-sdk-version]', (_c = {},
                    _c['new-sdk-version'] = newSdkVersion,
                    _c))
                : locale_1.tct('update your SDK from @v[sdk-version] to @v[new-sdk-version]', (_d = {},
                    _d['sdk-version'] = sdk.version,
                    _d['new-sdk-version'] = newSdkVersion,
                    _d))
            : locale_1.t('update your SDK version');
    }
    var getTitleData = function () {
        switch (suggestion.type) {
            case 'updateSdk':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.sdkUrl,
                    content: getUpdateSdkContent(suggestion.newSdkVersion),
                };
            case 'changeSdk':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.sdkUrl,
                    content: locale_1.tct('migrate to the [sdkName] SDK', {
                        sdkName: <code>{suggestion.newSdkName}</code>,
                    }),
                };
            case 'enableIntegration':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.integrationUrl,
                    content: locale_1.t("enable the '%s' integration", suggestion.integrationName),
                };
            default:
                return null;
        }
    };
    var getTitle = function () {
        var titleData = getTitleData();
        if (!titleData) {
            return null;
        }
        var href = titleData.href, content = titleData.content;
        if (!href) {
            return content;
        }
        return <externalLink_1.default href={href}>{content}</externalLink_1.default>;
    };
    var title = <react_1.Fragment>{getTitle()}</react_1.Fragment>;
    if (!suggestion.enables.length) {
        return title;
    }
    var alertContent = suggestion.enables
        .map(function (subSuggestion, index) {
        var subSuggestionContent = getSdkUpdateSuggestion({
            suggestion: subSuggestion,
            sdk: sdk,
        });
        if (!subSuggestionContent) {
            return null;
        }
        return <react_1.Fragment key={index}>{subSuggestionContent}</react_1.Fragment>;
    })
        .filter(function (content) { return !!content; });
    if (!alertContent.length) {
        return title;
    }
    return locale_1.tct('[title] so you can: [suggestion]', {
        title: title,
        suggestion: <AlertUl>{alertContent}</AlertUl>,
    });
}
exports.default = getSdkUpdateSuggestion;
var AlertUl = styled_1.default('ul')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n  margin-bottom: ", ";\n  padding-left: 0 !important;\n"], ["\n  margin-top: ", ";\n  margin-bottom: ", ";\n  padding-left: 0 !important;\n"])), space_1.default(1), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=getSdkUpdateSuggestion.jsx.map