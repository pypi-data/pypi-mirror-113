Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/events/styles");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var screenshot_1 = tslib_1.__importDefault(require("./screenshot"));
var tags_1 = tslib_1.__importDefault(require("./tags"));
function EventTagsAndScreenshots(_a) {
    var projectSlug = _a.projectId, isShare = _a.isShare, hasContext = _a.hasContext, hasQueryFeature = _a.hasQueryFeature, location = _a.location, isBorderless = _a.isBorderless, event = _a.event, props = tslib_1.__rest(_a, ["projectId", "isShare", "hasContext", "hasQueryFeature", "location", "isBorderless", "event"]);
    var _b = event.tags, tags = _b === void 0 ? [] : _b;
    if (!tags.length && !hasContext && isShare) {
        return null;
    }
    return (<Wrapper isBorderless={isBorderless}>
      {!isShare && <screenshot_1.default {...props} event={event} projectSlug={projectSlug}/>}
      <tags_1.default {...props} event={event} projectSlug={projectSlug} hasContext={hasContext} hasQueryFeature={hasQueryFeature} location={location}/>
    </Wrapper>);
}
exports.default = EventTagsAndScreenshots;
var Wrapper = styled_1.default(styles_1.DataSection)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (max-width: ", ") {\n    && {\n      padding: 0;\n      border: 0;\n    }\n  }\n\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n    grid-template-columns: auto minmax(0, 1fr);\n    grid-gap: ", ";\n\n    > *:first-child {\n      border-bottom: 0;\n      padding-bottom: 0;\n    }\n  }\n\n  ", "\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (max-width: ", ") {\n    && {\n      padding: 0;\n      border: 0;\n    }\n  }\n\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n    grid-template-columns: auto minmax(0, 1fr);\n    grid-gap: ", ";\n\n    > *:first-child {\n      border-bottom: 0;\n      padding-bottom: 0;\n    }\n  }\n\n  ", "\n"])), space_1.default(3), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(2), space_1.default(4), function (p) {
    return p.isBorderless &&
        "\n    && {\n        padding: " + space_1.default(3) + " 0 0 0;\n        :first-child {\n          padding-top: 0;\n          border-top: 0;\n        }\n      }\n    ";
});
var templateObject_1;
//# sourceMappingURL=index.jsx.map