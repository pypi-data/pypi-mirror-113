"""
"Composition" approach

Pros: dev can pick and choose what works for particular scenario,
      doesn't have to learn everything at once just to get started
Cons: Less structure so less is handled automatically, and might be harder to couple functionality
"""


@datafunction(namespace="shopify")
class ShopifyImporter(Importer):
    api = ApiConnection(auth=BearerToken)
    pagination = CursorPagination(key="cursor")
    response_handler = JsonResponse(key="orders")
    state_manager = UpdatedAtStateManager(field_name="updated_at")
    schema = ShopifyOrder


@datafunction(
    "import_orders",
    namespace="shopify",
    display_name="Import Shopify orders",
)
def import_orders(
    ctx: Context,
    admin_url: str,
) -> Iterator[Records[ShopifyOrder]]:

    conn = ApiConnection(headers={}, params={}, basic_auth={})

    handler = JsonResponse(key="orders", pagination=CursorPagination(name="cursor"))
    # handler = FileResponse(format="csv", pagination=NumberPagination(name="page"))
    # handler = XmlResponse()

    state_manager = IncrementalByModificationOrder()
    # state_manager = ReimportAllByCursor()
    # state_manager = ReimportAllPeriodic()
    # state_manager = IncrementalByCreationOrder()
    # state_manager = IncrementalByCreationOrderWithRefreshWindow()

    resp = None
    req = None
    state = state_manager.get_state()
    # update request with state
    while ctx.should_continue():
        req = pagination.get_next_request(req, resp)
        if req is None:
            break
        # update request with state if makes sense
        resp = conn.get(req)
        if handler.is_empty_response(resp):
            break
        records = handler.get_records(resp)
        yield records
        state = state_manager.update_state(ctx, req, resp, records)


"""
"A la carte" approach

Pros: dev can pick and choose what works for particular scenario,
      doesn't have to learn everything at once just to get started
Cons: Less structure so less is handled automatically, and might be harder to couple functionality
"""


@datafunction(
    "import_orders",
    namespace="shopify",
    display_name="Import Shopify orders",
)
def import_orders(
    ctx: Context,
    admin_url: str,
) -> Iterator[Records[ShopifyOrder]]:
    conn = ApiConnectioon(ctx)
    handler = JsonHandler(key="orders")
    state = UpdatedAtStateManager()
    resp = None
    params = {}
    while ctx.should_continue():
        req = handler.get_next_request(params, resp)
        if req is None:
            break
        # state.update_request(req) -- something here
        resp = conn.get(req)
        if handler.is_empty_response():
            break
        records = handler.get_records(resp)
        yield records
        state.update_state(ctx, req, resp, records)


"""
"MEGA-Class" approach -- put everything into an Importer subclass.

Pros: everything handled in one place, can couple logic
Cons: less flexible, constantly have to modify super-class to make it work for new paradigm
"""


@datafunction(
    "import_orders",
    namespace="shopify",
    display_name="Import Shopify orders",
)
def import_orders(
    ctx: Context,
    admin_url: str,
) -> Iterator[Records[ShopifyOrder]]:
    """Import Shopify orders

    Params:
        admin_url: Admin url from a "private app", of the form 'https://23dke3....:dkK29....@your-shop.myshopify.com'
    """
    importer = ShopifyImporter(ctx)
    resp = None
    while ctx.should_continue():
        req = importer.get_next_request(ctx, prev_response=resp)
        if req is None:
            break
        resp = importer.get_response(req)
        if not importer.is_empty_response():
            break
        records = importer.get_records_object(resp)
        yield records
        importer.update_state(ctx, req, resp, records)
