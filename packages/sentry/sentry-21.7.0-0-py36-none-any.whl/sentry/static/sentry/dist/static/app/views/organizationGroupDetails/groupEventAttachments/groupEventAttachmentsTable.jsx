Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var locale_1 = require("app/locale");
var groupEventAttachmentsTableRow_1 = tslib_1.__importDefault(require("app/views/organizationGroupDetails/groupEventAttachments/groupEventAttachmentsTableRow"));
var GroupEventAttachmentsTable = function (_a) {
    var attachments = _a.attachments, orgId = _a.orgId, projectId = _a.projectId, groupId = _a.groupId, onDelete = _a.onDelete, deletedAttachments = _a.deletedAttachments;
    var tableRowNames = [locale_1.t('Name'), locale_1.t('Type'), locale_1.t('Size'), locale_1.t('Actions')];
    return (<table className="table events-table">
      <thead>
        <tr>
          {tableRowNames.map(function (name) { return (<th key={name}>{name}</th>); })}
        </tr>
      </thead>
      <tbody>
        {attachments.map(function (attachment) { return (<groupEventAttachmentsTableRow_1.default key={attachment.id} attachment={attachment} orgId={orgId} projectId={projectId} groupId={groupId} onDelete={onDelete} isDeleted={deletedAttachments.some(function (id) { return attachment.id === id; })}/>); })}
      </tbody>
    </table>);
};
exports.default = GroupEventAttachmentsTable;
//# sourceMappingURL=groupEventAttachmentsTable.jsx.map