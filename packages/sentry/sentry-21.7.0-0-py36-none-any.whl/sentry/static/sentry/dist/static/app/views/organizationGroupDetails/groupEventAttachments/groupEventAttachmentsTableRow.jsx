Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var eventAttachmentActions_1 = tslib_1.__importDefault(require("app/components/events/eventAttachmentActions"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var locale_1 = require("app/locale");
var attachmentUrl_1 = tslib_1.__importDefault(require("app/utils/attachmentUrl"));
var types_1 = require("app/views/organizationGroupDetails/groupEventAttachments/types");
var GroupEventAttachmentsTableRow = function (_a) {
    var attachment = _a.attachment, projectId = _a.projectId, onDelete = _a.onDelete, isDeleted = _a.isDeleted, orgId = _a.orgId, groupId = _a.groupId;
    return (<TableRow isDeleted={isDeleted}>
    <td>
      <h5>
        {attachment.name}
        <br />
        <small>
          <dateTime_1.default date={attachment.dateCreated}/> &middot;{' '}
          <link_1.default to={"/organizations/" + orgId + "/issues/" + groupId + "/events/" + attachment.event_id + "/"}>
            {attachment.event_id}
          </link_1.default>
        </small>
      </h5>
    </td>

    <td>{types_1.types[attachment.type] || locale_1.t('Other')}</td>

    <td>
      <fileSize_1.default bytes={attachment.size}/>
    </td>

    <td>
      <ActionsWrapper>
        <attachmentUrl_1.default projectId={projectId} eventId={attachment.event_id} attachment={attachment}>
          {function (url) {
            return !isDeleted && (<eventAttachmentActions_1.default url={url} onDelete={onDelete} attachmentId={attachment.id}/>);
        }}
        </attachmentUrl_1.default>
      </ActionsWrapper>
    </td>
  </TableRow>);
};
var TableRow = styled_1.default('tr')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  opacity: ", ";\n  td {\n    text-decoration: ", ";\n  }\n"], ["\n  opacity: ", ";\n  td {\n    text-decoration: ", ";\n  }\n"])), function (p) { return (p.isDeleted ? 0.3 : 1); }, function (p) { return (p.isDeleted ? 'line-through' : 'normal'); });
var ActionsWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n"], ["\n  display: inline-block;\n"])));
exports.default = GroupEventAttachmentsTableRow;
var templateObject_1, templateObject_2;
//# sourceMappingURL=groupEventAttachmentsTableRow.jsx.map