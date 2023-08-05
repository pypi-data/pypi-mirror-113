Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var eventsTableRow_1 = tslib_1.__importDefault(require("app/components/eventsTable/eventsTableRow"));
var locale_1 = require("app/locale");
var EventsTable = /** @class */ (function (_super) {
    tslib_1.__extends(EventsTable, _super);
    function EventsTable() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventsTable.prototype.render = function () {
        var _a = this.props, events = _a.events, tagList = _a.tagList, orgId = _a.orgId, projectId = _a.projectId, groupId = _a.groupId;
        var hasUser = !!events.find(function (event) { return event.user; });
        return (<table className="table events-table">
        <thead>
          <tr>
            <th>{locale_1.t('ID')}</th>
            {hasUser && <th>{locale_1.t('User')}</th>}

            {tagList.map(function (tag) { return (<th key={tag.key}>{tag.name}</th>); })}
          </tr>
        </thead>
        <tbody>
          {events.map(function (event) { return (<eventsTableRow_1.default key={event.id} event={event} orgId={orgId} projectId={projectId} groupId={groupId} tagList={tagList} hasUser={hasUser}/>); })}
        </tbody>
      </table>);
    };
    return EventsTable;
}(react_1.Component));
exports.default = EventsTable;
//# sourceMappingURL=eventsTable.jsx.map