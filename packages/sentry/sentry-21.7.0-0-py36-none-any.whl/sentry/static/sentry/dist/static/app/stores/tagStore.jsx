Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var tagActions_1 = tslib_1.__importDefault(require("app/actions/tagActions"));
// This list is only used on issues. Events/discover
// have their own field list that exists elsewhere.
// contexts.key and contexts.value omitted on purpose.
var BUILTIN_TAGS = [
    'event.type',
    'platform',
    'message',
    'title',
    'location',
    'timestamp',
    'release',
    'user.id',
    'user.username',
    'user.email',
    'user.ip',
    'sdk.name',
    'sdk.version',
    'http.method',
    'http.url',
    'os.build',
    'os.kernel_version',
    'device.brand',
    'device.locale',
    'device.uuid',
    'device.model_id',
    'device.arch',
    'device.orientation',
    'geo.country_code',
    'geo.region',
    'geo.city',
    'error.type',
    'error.handled',
    'error.unhandled',
    'error.value',
    'error.mechanism',
    'stack.abs_path',
    'stack.filename',
    'stack.package',
    'stack.module',
    'stack.function',
    'stack.stack_level',
].reduce(function (acc, tag) {
    acc[tag] = { key: tag, name: tag };
    return acc;
}, {});
var tagStoreConfig = {
    state: {},
    init: function () {
        this.state = {};
        this.listenTo(tagActions_1.default.loadTagsSuccess, this.onLoadTagsSuccess);
    },
    getBuiltInTags: function () {
        return tslib_1.__assign({}, BUILTIN_TAGS);
    },
    getIssueAttributes: function () {
        // TODO(mitsuhiko): what do we do with translations here?
        var isSuggestions = [
            'resolved',
            'unresolved',
            'ignored',
            'assigned',
            'for_review',
            'unassigned',
            'linked',
            'unlinked',
        ];
        return {
            is: {
                key: 'is',
                name: 'Status',
                values: isSuggestions,
                maxSuggestedValues: isSuggestions.length,
                predefined: true,
            },
            has: {
                key: 'has',
                name: 'Has Tag',
                values: Object.keys(this.state),
                predefined: true,
            },
            assigned: {
                key: 'assigned',
                name: 'Assigned To',
                values: [],
                predefined: true,
            },
            bookmarks: {
                key: 'bookmarks',
                name: 'Bookmarked By',
                values: [],
                predefined: true,
            },
            lastSeen: {
                key: 'lastSeen',
                name: 'Last Seen',
                values: ['-1h', '+1d', '-1w'],
                predefined: true,
            },
            firstSeen: {
                key: 'firstSeen',
                name: 'First Seen',
                values: ['-1h', '+1d', '-1w'],
                predefined: true,
            },
            firstRelease: {
                key: 'firstRelease',
                name: 'First Release',
                values: ['latest'],
                predefined: true,
            },
            'event.timestamp': {
                key: 'event.timestamp',
                name: 'Event Timestamp',
                values: ['2017-01-02', '>=2017-01-02T01:00:00', '<2017-01-02T02:00:00'],
                predefined: true,
            },
            timesSeen: {
                key: 'timesSeen',
                name: 'Times Seen',
                isInput: true,
                // Below values are required or else SearchBar will attempt to get values // This is required or else SearchBar will attempt to get values
                values: [],
                predefined: true,
            },
            assigned_or_suggested: {
                key: 'assigned_or_suggested',
                name: 'Assigned or Suggested',
                isInput: true,
                values: [],
                predefined: true,
            },
        };
    },
    reset: function () {
        this.state = {};
        this.trigger(this.state);
    },
    getAllTags: function () {
        return this.state;
    },
    onLoadTagsSuccess: function (data) {
        var newTags = data.reduce(function (acc, tag) {
            acc[tag.key] = tslib_1.__assign({ values: [] }, tag);
            return acc;
        }, {});
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), newTags);
        this.trigger(this.state);
    },
};
var TagStore = reflux_1.default.createStore(tagStoreConfig);
exports.default = TagStore;
//# sourceMappingURL=tagStore.jsx.map