Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
/**
 * Render metadata about the event and provide a link to the JSON blob.
 * Used in the sidebar of performance event details and discover2 event details.
 */
function EventMetadata(_a) {
    var event = _a.event, organization = _a.organization, projectId = _a.projectId;
    var eventJsonUrl = "/api/0/projects/" + organization.slug + "/" + projectId + "/events/" + event.eventID + "/json/";
    return (<MetaDataID>
      <styles_1.SectionHeading>{locale_1.t('Event ID')}</styles_1.SectionHeading>
      <MetadataContainer data-test-id="event-id">{event.eventID}</MetadataContainer>
      <MetadataContainer>
        <dateTime_1.default date={getDynamicText_1.default({
            value: event.dateCreated || (event.endTimestamp || 0) * 1000,
            fixed: 'Dummy timestamp',
        })}/>
      </MetadataContainer>
      <projects_1.default orgId={organization.slug} slugs={[projectId]}>
        {function (_a) {
            var projects = _a.projects;
            var project = projects.find(function (p) { return p.slug === projectId; });
            return (<StyledProjectBadge project={project ? project : { slug: projectId }} avatarSize={16}/>);
        }}
      </projects_1.default>
      <MetadataJSON href={eventJsonUrl} className="json-link">
        {locale_1.t('Preview JSON')} (<fileSize_1.default bytes={event.size}/>)
      </MetadataJSON>
    </MetaDataID>);
}
var MetaDataID = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(4));
var MetadataContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var MetadataJSON = styled_1.default(externalLink_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledProjectBadge = styled_1.default(projectBadge_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
exports.default = EventMetadata;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=eventMetadata.jsx.map