Object.defineProperty(exports, "__esModule", { value: true });
exports.EventsTableRow = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var deviceName_1 = tslib_1.__importDefault(require("app/components/deviceName"));
var fileSize_1 = tslib_1.__importDefault(require("app/components/fileSize"));
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var attachmentUrl_1 = tslib_1.__importDefault(require("app/utils/attachmentUrl"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var EventsTableRow = /** @class */ (function (_super) {
    tslib_1.__extends(EventsTableRow, _super);
    function EventsTableRow() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventsTableRow.prototype.renderCrashFileLink = function () {
        var _a = this.props, event = _a.event, projectId = _a.projectId;
        if (!event.crashFile) {
            return null;
        }
        var crashFileType = event.crashFile.type === 'event.minidump' ? 'Minidump' : 'Crash file';
        return (<attachmentUrl_1.default projectId={projectId} eventId={event.id} attachment={event.crashFile}>
        {function (url) {
                var _a, _b;
                return url && (<small>
              {crashFileType}: <a href={url + "?download=1"}>{(_a = event.crashFile) === null || _a === void 0 ? void 0 : _a.name}</a> (
              <fileSize_1.default bytes={((_b = event.crashFile) === null || _b === void 0 ? void 0 : _b.size) || 0}/>)
            </small>);
            }}
      </attachmentUrl_1.default>);
    };
    EventsTableRow.prototype.render = function () {
        var _a = this.props, className = _a.className, event = _a.event, orgId = _a.orgId, groupId = _a.groupId, tagList = _a.tagList, hasUser = _a.hasUser;
        var tagMap = {};
        event.tags.forEach(function (tag) {
            tagMap[tag.key] = tag.value;
        });
        var link = "/organizations/" + orgId + "/issues/" + groupId + "/events/" + event.id + "/";
        return (<tr key={event.id} className={className}>
        <td>
          <h5>
            <globalSelectionLink_1.default to={link}>
              <dateTime_1.default date={event.dateCreated}/>
            </globalSelectionLink_1.default>
            <small>{event.title.substr(0, 100)}</small>
            {this.renderCrashFileLink()}
          </h5>
        </td>

        {hasUser && (<td className="event-user table-user-info">
            {event.user ? (<div>
                <userAvatar_1.default user={event.user} // TODO(ts): Some of the user fields are optional from event, this cast can probably be removed in the future
                 size={24} className="avatar" gravatar={false}/>
                {event.user.email}
              </div>) : (<span>—</span>)}
          </td>)}

        {tagList.map(function (tag) { return (<td key={tag.key}>
            <div>
              {tag.key === 'device' ? (<deviceName_1.default value={tagMap[tag.key]}/>) : (tagMap[tag.key])}
            </div>
          </td>); })}
      </tr>);
    };
    return EventsTableRow;
}(React.Component));
exports.EventsTableRow = EventsTableRow;
exports.default = withOrganization_1.default(EventsTableRow);
//# sourceMappingURL=eventsTableRow.jsx.map