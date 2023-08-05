Object.defineProperty(exports, "__esModule", { value: true });
exports.OpenInName = exports.OpenInLink = exports.OpenInContainer = exports.OpenInContextLine = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var sentryAppIcon_1 = require("app/components/sentryAppIcon");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var queryString_1 = require("app/utils/queryString");
var recordSentryAppInteraction_1 = require("app/utils/recordSentryAppInteraction");
var OpenInContextLine = function (_a) {
    var lineNo = _a.lineNo, filename = _a.filename, components = _a.components;
    var handleRecordInteraction = function (slug) { return function () {
        recordSentryAppInteraction_1.recordInteraction(slug, 'sentry_app_component_interacted', {
            componentType: 'stacktrace-link',
        });
    }; };
    var getUrl = function (url) {
        return queryString_1.addQueryParamsToExistingUrl(url, { lineNo: lineNo, filename: filename });
    };
    return (<exports.OpenInContainer columnQuantity={components.length + 1}>
      <div>{locale_1.t('Open this line in')}</div>
      {components.map(function (component) {
            var url = getUrl(component.schema.url);
            var slug = component.sentryApp.slug;
            var onClickRecordInteraction = handleRecordInteraction(slug);
            return (<exports.OpenInLink key={component.uuid} data-test-id={"stacktrace-link-" + slug} href={url} onClick={onClickRecordInteraction} onContextMenu={onClickRecordInteraction} openInNewTab>
            <sentryAppIcon_1.SentryAppIcon slug={slug}/>
            <exports.OpenInName>{locale_1.t("" + component.sentryApp.name)}</exports.OpenInName>
          </exports.OpenInLink>);
        })}
    </exports.OpenInContainer>);
};
exports.OpenInContextLine = OpenInContextLine;
exports.OpenInContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  z-index: 1;\n  display: grid;\n  grid-template-columns: repeat(", ", max-content);\n  grid-gap: ", ";\n  color: ", ";\n  background-color: ", ";\n  font-family: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  box-shadow: ", ";\n  text-indent: initial;\n  overflow: auto;\n  white-space: nowrap;\n"], ["\n  position: relative;\n  z-index: 1;\n  display: grid;\n  grid-template-columns: repeat(", ", max-content);\n  grid-gap: ", ";\n  color: ", ";\n  background-color: ", ";\n  font-family: ", ";\n  border-bottom: 1px solid ", ";\n  padding: ", " ", ";\n  box-shadow: ", ";\n  text-indent: initial;\n  overflow: auto;\n  white-space: nowrap;\n"])), function (p) { return p.columnQuantity; }, space_1.default(1), function (p) { return p.theme.subText; }, function (p) { return p.theme.background; }, function (p) { return p.theme.text.family; }, function (p) { return p.theme.border; }, space_1.default(0.25), space_1.default(3), function (p) { return p.theme.dropShadowLightest; });
exports.OpenInLink = styled_1.default(externalLink_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  align-items: center;\n  grid-template-columns: max-content auto;\n  grid-gap: ", ";\n  color: ", ";\n"], ["\n  display: inline-grid;\n  align-items: center;\n  grid-template-columns: max-content auto;\n  grid-gap: ", ";\n  color: ", ";\n"])), space_1.default(0.75), function (p) { return p.theme.gray300; });
exports.OpenInName = styled_1.default('strong')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-weight: 700;\n"], ["\n  color: ", ";\n  font-weight: 700;\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=openInContextLine.jsx.map