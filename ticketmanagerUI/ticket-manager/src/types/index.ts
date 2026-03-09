export const StatusMap: Record<string, string> = {
    '4FAF6585-8EFC-4AD4-AEDD-159A1D2FF57B': 'Active',
    '5D95CD40-3755-489C-9978-F1A53D62845E': 'Closed',
    'A53C14A8-F113-46EF-A634-269484A1AABE': 'Open'
};

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export interface UserLogin {
    Email: string;
    Password: string;
}

export interface UserCreate {
    Name: string;
    Email: string;
    Password: string;
}

export interface TicketResponse {
    UID: string;
    Title: string;
    Description: string;
    StatusUID: string;
    Priority: string;
    CreatorUID: string;
    AssigneeUID: string | null;
    CreatedAt: string;
    UpdatedAt: string;
}
