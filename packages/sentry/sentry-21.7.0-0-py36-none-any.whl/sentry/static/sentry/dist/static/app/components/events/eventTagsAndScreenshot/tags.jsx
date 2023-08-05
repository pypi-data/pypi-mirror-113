Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var eventDataSection_1 = require("app/components/events/eventDataSection");
var locale_1 = require("app/locale");
var eventTags_1 = tslib_1.__importDefault(require("../eventTags/eventTags"));
var dataSection_1 = tslib_1.__importDefault(require("./dataSection"));
var tagsHighlight_1 = tslib_1.__importDefault(require("./tagsHighlight"));
function Tags(_a) {
    var event = _a.event, organization = _a.organization, projectSlug = _a.projectSlug, location = _a.location, hasContext = _a.hasContext, hasQueryFeature = _a.hasQueryFeature;
    return (<StyledDataSection title={locale_1.t('Tags')} description={locale_1.t('Tags help you quickly both access related events and view the tag distribution for a set of events')}>
      {hasContext && <tagsHighlight_1.default event={event}/>}
      <eventTags_1.default event={event} organization={organization} projectId={projectSlug} location={location} hasQueryFeature={hasQueryFeature}/>
    </StyledDataSection>);
}
exports.default = Tags;
var StyledDataSection = styled_1.default(dataSection_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", " {\n    overflow: hidden;\n  }\n"], ["\n  ", " {\n    overflow: hidden;\n  }\n"])), eventDataSection_1.SectionContents);
var templateObject_1;
//# sourceMappingURL=tags.jsx.map